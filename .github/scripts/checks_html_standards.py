"""
checks_html_standards.py — index.html standards/safety hygiene + webmanifest + asset integrity checks (324-337)
(extracted from check_repository_consistency.py — check.py split track).

run(ctx) receives shared check()/ROOT by reference (exec 不使用) so exit code / BLOCKING propagation
are byte-equivalent. annotation+def-aware free-var 分析で外部 `_`-var・global-content 依存ゼロ確認済。
nested-fn の module-level `global _accNNN` は run() 内で `nonlocal` へ機械変換 (意味等価)。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  324. `.well-known/aio-manifest.json` `entity.affiliation.start_date`
       MUST NOT be in the future (relative to today, JST). Drift = a
       timezone slip or typo yielding a future employment start date,
       which readers interpret as either "not yet employed" (contradicts
       the site's affiliation narrative) or "content from the future"
       (recency ranking corruption). Sibling of Check 313 (generated_at +
       last_metadata_update not future) / Check 236 (start_date ISO
       format) for the affiliation start_date recency axis. (BLOCKING)

  325. `index.html` `<meta name="referrer">` MUST be present AND its
       content value MUST be in the W3C Referrer Policy enumeration:
       `{no-referrer, no-referrer-when-downgrade, origin,
       origin-when-cross-origin, same-origin, strict-origin,
       strict-origin-when-cross-origin, unsafe-url}`. Drift = missing
       meta silently falls back to browser default (typically
       `strict-origin-when-cross-origin` on modern UAs, but older/embedded
       browsers may leak full URL); a typo (`same origin`) is spec-
       invalid and browsers ignore silently, again falling back to
       default. Sibling of Check 115 (CSP hardening baseline) / Check 249
       (viewport spec compliance) for the HTTP-header-equivalent security
       meta axis. (BLOCKING)

  326. `index.html` every `<link rel="preload" as="X">` `as` value MUST
       be in the HTML5 preload destination enumeration: `{audio,
       document, embed, fetch, font, image, object, script, style, track,
       video, worker}`. Drift = a typo (`styles` / `img`) silently makes
       the browser IGNORE the preload hint (per spec, invalid as= yields
       ignored preload) → first-paint regression, wasted download or
       double-fetch. Check 73a enforces `as=` presence; this Check
       enforces its VALUE. Sibling of Check 73a (as= presence) /
       Check 158 (Google Fonts preconnect) for the preload structural
       correctness axis. (BLOCKING)

  327. `index.html` MUST NOT contain any `<meta http-equiv="refresh">`
       element. Drift = an accidental redirect meta creates:
       (a) SEO harm — Google treats meta refresh with 0-second delay as
           a soft 301 but with delay > 0 loses PageRank transfer,
       (b) a11y regression — screen readers cannot cancel automatic
           refreshes, WCAG 2.2.1 (Timing Adjustable) violation,
       (c) AI crawler confusion — content and metadata point at different
           URLs.
       Sibling of Check 325 (referrer policy) / Check 322 (inline style)
       for the HTML negative-invariant surface axis. (BLOCKING)

  328. `index.html` MUST NOT contain any `<base>` element. Drift = an
       accidental `<base href="/other/">` silently rewrites the resolution
       of every relative URL in the document, breaking:
       (a) SPA routing — `./#/route` hash-navigation depends on the
           current document URL not the `<base>` href,
       (b) `./` asset references (icon.svg, main.js, style.css) resolve
           to a different origin/path than intended,
       (c) canonical URL semantics: JSON-LD @id + `<link rel="canonical">`
           become de-synced with the document's effective base.
       Sibling of Check 327 (no meta refresh) / Check 322 (no inline
       style) for the HTML SPA-integrity negative-invariant axis.
       (BLOCKING)

  329. `index.html` MUST NOT contain any HTML4 obsolete / deprecated
       element: `<frame>`, `<frameset>`, `<applet>`, `<font>`, `<center>`,
       `<blink>`, `<marquee>`, `<big>`, `<strike>`. Drift = an
       accidental deprecated element:
       (a) breaks HTML5 validators and static analyzers,
       (b) yields inconsistent rendering across UAs (some ignore, some
           polyfill with layout differences),
       (c) contradicts the site's "modern Boring Technology" narrative,
       (d) `<applet>` is a Java plugin attack surface, `<frame>` breaks
           SPA hash router.
       Sibling of Check 328 (no `<base>`) / Check 327 (no meta refresh)
       for the HTML modernity + hygiene negative-invariant axis.
       (BLOCKING)

  330. `index.html` MUST NOT contain `<iframe>`, `<object>`, or `<embed>`
       elements. Drift = an accidental external-content embed:
       (a) opens a cross-origin attack surface (embedded document can
           trigger click-jacking, phishing, or drive-by download),
       (b) requires expanding CSP `frame-src` / `object-src` allowlists,
       (c) inconsistent rendering (Safari's plugin sandbox differs from
           Chrome, screen readers announce inconsistently),
       (d) breaks the "Boring Technology single-document SPA" narrative.
       Sibling of Check 329 (HTML4 deprecated) / Check 115 (CSP
       hardening) for the HTML external-embed attack-surface axis.
       (BLOCKING)

  331. `index.html` MUST NOT contain any HTML attribute whose value starts
       with `javascript:` (e.g. `href="javascript:..."`, `src="javascript:..."`,
       `formaction="javascript:..."`). Drift = a JS URL scheme silently
       bypasses CSP `script-src` (executes in the anchor's context) and
       forms a persistent XSS vector even under strict CSP. Sibling of
       Check 239 (no eval/Function) / Check 242 (inline `on*=` handler
       allowlist) / Check 323 (no `style=`) for the HTML JS-URL-scheme
       zero-tolerance axis. (BLOCKING)

  332. Root scripts (`aio-guard.js`, `theme-init.js`, `karte-init.js`,
       `error-suppressor.js`) MUST NOT contain `import` or `export`
       statements. index.html loads these as CLASSIC `<script>` (not
       `<script type="module">`) so any ESM statement causes a silent
       parse error and the whole script is dropped. Drift class:
       - theme-init.js parse-fail = FOUC on first paint (pre-paint theme
         attribute never applied)
       - error-suppressor.js parse-fail = known-benign errors surface as
         FatalPage
       - aio-guard.js parse-fail = AIO asset-anchor self-repair monitor
         disabled
       - karte-init.js parse-fail = analytics stub unavailable
       Sibling of Check 239 (no eval) / Check 43d (main.js single IIFE)
       for the shipped-JS module-boundary integrity axis. (BLOCKING)

  333. `manifest.webmanifest` `name` / `short_name` / `description` MUST
       NOT contain the real name (`横井雄太` / `Yokoi Yuta` / `Yuta Yokoi`).
       The PWA install prompt / app launcher label is a general-public UI
       surface subject to the same anonymity contract as the visual site
       (Check 124 — UI displays "yuta", real name is AIO/entity layer
       only). Drift = a webmanifest edit leaks the real name onto every
       user's home screen / app switcher. Sibling of Check 124 (visible
       renderer anonymity) for the PWA-surface anonymity axis. (BLOCKING)

  334. `manifest.webmanifest` `orientation` MUST be in the W3C Web App
       Manifest spec enumeration: `{any, natural, landscape,
       landscape-primary, landscape-secondary, portrait, portrait-primary,
       portrait-secondary}`. Drift = a typo (`landscpae` / `horizontal`)
       is spec-invalid; the UA ignores it and falls back to the platform
       default, silently losing the intended orientation lock. Sibling of
       Check 315 (display enum) / Check 316 (icons purpose enum) for the
       webmanifest structural correctness axis. (BLOCKING)

  335. `index.html` MUST contain a `<link rel="manifest">` whose href
       resolves (after stripping the canonical URL pathname prefix) to the
       actual `manifest.webmanifest` file in the repo. Drift = removing
       the link tag OR drifting its href silently disables the entire PWA
       install capability — no install prompt, no home-screen icon, no
       standalone launch — and NO gate catches it (behavior e2e does not
       test PWA install; the screenshot is advisory). Check 210–316 verify
       the webmanifest's CONTENT but assume it is wired; this Check closes
       the wiring leak. Sibling of Check 135 (stylesheet `<link>` wiring)
       / Check 134 (root script wiring) for the webmanifest link-wiring
       axis. (BLOCKING)

  336. `<meta property="og:image">` and `<meta name="twitter:image">`
       content URLs MUST be byte-identical (single canonical social-card
       image). Drift = og:image and twitter:image point at two different
       (individually valid, canonical, resolving) images — a Twitter card
       preview shows one image while LinkedIn/Slack/Facebook OG consumers
       show another, fracturing the entity's visual identity across social
       surfaces. Check 153 (both canonical-prefixed) / Check 164 (both
       resolve to a file) allow this drift because each URL is valid in
       isolation. Sibling of Check 155 (og:title ↔ twitter:title) for the
       social-card image-coherence axis. (BLOCKING)

  337. Canonical binary assets MUST have magic bytes matching their file
       extension: `yuta-yokoi-ai-pm-orchestration-system.webp` MUST start
       with RIFF....WEBP (bytes 0-3 = `RIFF`, bytes 8-11 = `WEBP`), and
       `yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3` MUST start
       with `ID3` or an MPEG frame-sync (`0xFF 0xEx`/`0xFx`). Drift = a
       file gets replaced by a different format while keeping its
       extension (e.g. a PNG saved as `.webp`); the byte-budget check
       (Check 269) passes since it only measures size, but strict crawlers
       and browsers that sniff content-type reject or mis-render it.
       Sibling of Check 269 (binary byte budget) / Check 42 (digest chain)
       for the binary-asset format-integrity axis. (BLOCKING)

"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 324. aio-manifest affiliation.start_date NOT future (BLOCKING) ───────────
    _mani324 = ROOT / ".well-known" / "aio-manifest.json"
    if _mani324.exists():
        from datetime import date as _date324
        try:
            _md324 = json.loads(_mani324.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _md324 = None
        if _md324 is not None:
            _sd324 = str(
                _md324.get("entity", {}).get("affiliation", {}).get("start_date", "")
            )
            _today324 = _date324.today()
            _future324 = False
            _detail324 = _sd324
            if re.match(r"^\d{4}-\d{2}-\d{2}$", _sd324):
                try:
                    _future324 = _date324.fromisoformat(_sd324) > _today324
                except ValueError:
                    pass
            _ok324 = bool(_sd324) and not _future324
            check(
                _ok324,
                f"Check 324: affiliation.start_date={_detail324!r} は今日以下 (today={_today324.isoformat()})",
                (f"Check 324: affiliation.start_date={_detail324!r} は今日 "
                 f"({_today324.isoformat()}) より未来 — 「未来から来た所属」矛盾 / "
                 "recency ranking corruption。today 以下へ修正"),
                blocking=True,
            )
        else:
            check(False, "Check 324: aio-manifest.json parseable",
                  "Check 324: aio-manifest.json が JSON parse 不能", blocking=True)
    else:
        check(False, "Check 324: aio-manifest.json present",
              "Check 324: aio-manifest.json が無い", blocking=True)

    # ── 325. index.html <meta name="referrer"> valid enum (BLOCKING) ─────────────
    _html325 = ROOT / "index.html"
    if _html325.exists():
        _hs325 = _html325.read_text(encoding="utf-8")
        _stripped325 = re.sub(r"<!--.*?-->", "", _hs325, flags=re.DOTALL)
        _m325a = re.search(
            r'<meta\s+name="referrer"[^>]*content="([^"]+)"', _stripped325)
        _m325b = re.search(
            r'<meta\s+content="([^"]+)"[^>]*name="referrer"', _stripped325)
        _val325 = None
        if _m325a: _val325 = _m325a.group(1)
        elif _m325b: _val325 = _m325b.group(1)
        _valid_enum325 = {
            "no-referrer", "no-referrer-when-downgrade", "origin",
            "origin-when-cross-origin", "same-origin", "strict-origin",
            "strict-origin-when-cross-origin", "unsafe-url",
        }
        _ok325 = _val325 is not None and _val325 in _valid_enum325
        check(
            _ok325,
            f"Check 325: <meta name=\"referrer\"> content={_val325!r} ∈ W3C enum",
            (f"Check 325: <meta name=\"referrer\"> {'missing' if _val325 is None else f'invalid={_val325!r}'} — "
             f"allowed={sorted(_valid_enum325)}。missing/invalid は browser default fallback "
             "(古い browser で full URL leak リスク)"),
            blocking=True,
        )
    else:
        check(False, "Check 325: index.html present",
              "Check 325: index.html が無い", blocking=True)

    # ── 326. <link rel="preload" as="X"> as value in HTML5 enum (BLOCKING) ───────
    _html326 = ROOT / "index.html"
    if _html326.exists():
        _hs326 = _html326.read_text(encoding="utf-8")
        _stripped326 = re.sub(r"<!--.*?-->", "", _hs326, flags=re.DOTALL)
        _preload_tags326 = re.findall(
            r'<link\s+[^>]*rel="preload"[^>]*>', _stripped326)
        _valid_as326 = {
            "audio", "document", "embed", "fetch", "font", "image",
            "object", "script", "style", "track", "video", "worker",
        }
        _bad_as326: list[str] = []
        _total_as326 = 0
        for _tag in _preload_tags326:
            _m_as = re.search(r'\bas="([^"]+)"', _tag)
            if not _m_as:
                continue  # Check 73a が as= 不在を担当
            _total_as326 += 1
            _val = _m_as.group(1)
            if _val not in _valid_as326:
                _bad_as326.append(f"as={_val!r} in tag={_tag[:80]!r}")
        _ok326 = (not _bad_as326) and _total_as326 > 0
        check(
            _ok326,
            f"Check 326: <link rel=\"preload\"> as= {_total_as326} 件すべて HTML5 enum 内",
            (f"Check 326: as= 値違反: {_bad_as326!r} — "
             f"allowed={sorted(_valid_as326)}。preload spec 違反で browser が hint を "
             "silent ignore し first-paint 回帰"),
            blocking=True,
        )
    else:
        check(False, "Check 326: index.html present",
              "Check 326: index.html が無い", blocking=True)

    # ── 327. index.html has zero <meta http-equiv="refresh"> (BLOCKING) ──────────
    _html327 = ROOT / "index.html"
    if _html327.exists():
        _hs327 = _html327.read_text(encoding="utf-8")
        _stripped327 = re.sub(r"<!--.*?-->", "", _hs327, flags=re.DOTALL)
        _refresh327 = re.findall(
            r'<meta\s+[^>]*http-equiv\s*=\s*["\']refresh["\']', _stripped327)
        _count327 = len(_refresh327)
        _ok327 = _count327 == 0
        check(
            _ok327,
            "Check 327: index.html <meta http-equiv=\"refresh\"> 0 件 (SEO/a11y 有害要素排除)",
            (f"Check 327: <meta http-equiv=\"refresh\"> が {_count327} 件検出 — "
             "SEO 有害 (PageRank 転移損失) / a11y 有害 (WCAG 2.2.1 timing 違反) / "
             "AI crawler の URL 混乱。redirect は server-side or SPA router に移行"),
            blocking=True,
        )
    else:
        check(False, "Check 327: index.html present",
              "Check 327: index.html が無い", blocking=True)

    # ── 328. index.html has zero <base> element (BLOCKING) ───────────────────────
    _html328 = ROOT / "index.html"
    if _html328.exists():
        _hs328 = _html328.read_text(encoding="utf-8")
        _stripped328 = re.sub(r"<!--.*?-->", "", _hs328, flags=re.DOTALL)
        # <base> element (self-closing含む) を検出。<baseline> のような word boundary case を除外。
        _base_tags328 = re.findall(r'<base\b[^>]*>', _stripped328, flags=re.IGNORECASE)
        _count328 = len(_base_tags328)
        _ok328 = _count328 == 0
        check(
            _ok328,
            "Check 328: index.html <base> element 0 件 (SPA relative URL 整合)",
            (f"Check 328: <base> element が {_count328} 件検出: {_base_tags328[:2]!r} — "
             "全 relative URL 解決が壊れ SPA hash router / ./asset 参照 / canonical "
             "semantics が破綻。<base> を削除して document URL に依拠せよ"),
            blocking=True,
        )
    else:
        check(False, "Check 328: index.html present",
              "Check 328: index.html が無い", blocking=True)

    # ── 329. index.html has no HTML4 deprecated tags (BLOCKING) ──────────────────
    _html329 = ROOT / "index.html"
    if _html329.exists():
        _hs329 = _html329.read_text(encoding="utf-8")
        _stripped329 = re.sub(r"<!--.*?-->", "", _hs329, flags=re.DOTALL)
        _deprecated329 = (
            "frame", "frameset", "applet", "font", "center",
            "blink", "marquee", "big", "strike",
        )
        _found329: dict[str, int] = {}
        for _tag in _deprecated329:
            _matches = re.findall(rf'<{_tag}\b', _stripped329, flags=re.IGNORECASE)
            if _matches:
                _found329[_tag] = len(_matches)
        _ok329 = not _found329
        check(
            _ok329,
            f"Check 329: index.html HTML4 deprecated tag 0 件 (対象 {len(_deprecated329)} 種類)",
            (f"Check 329: HTML4 deprecated tag 検出: {_found329!r} — "
             "HTML5 validator 破綻 / UA 描画差 / Boring Technology 契約矛盾。"
             "現代的な semantic tag へ置換せよ"),
            blocking=True,
        )
    else:
        check(False, "Check 329: index.html present",
              "Check 329: index.html が無い", blocking=True)

    # ── 330. index.html has no <iframe>/<object>/<embed> (BLOCKING) ──────────────
    _html330 = ROOT / "index.html"
    if _html330.exists():
        _hs330 = _html330.read_text(encoding="utf-8")
        _stripped330 = re.sub(r"<!--.*?-->", "", _hs330, flags=re.DOTALL)
        _embed_tags330 = ("iframe", "object", "embed")
        _found330: dict[str, int] = {}
        for _tag in _embed_tags330:
            _matches = re.findall(rf'<{_tag}\b', _stripped330, flags=re.IGNORECASE)
            if _matches:
                _found330[_tag] = len(_matches)
        _ok330 = not _found330
        check(
            _ok330,
            f"Check 330: index.html <iframe>/<object>/<embed> 0 件 (external-embed 攻撃面排除)",
            (f"Check 330: external-embed 要素検出: {_found330!r} — "
             "click-jacking / CSP frame-src 拡張 / render 差 / SPA narrative 崩壊。"
             "external content は WebView 化するか削除せよ"),
            blocking=True,
        )
    else:
        check(False, "Check 330: index.html present",
              "Check 330: index.html が無い", blocking=True)

    # ── 331. index.html no attribute="javascript:..." (BLOCKING) ─────────────────
    _html331 = ROOT / "index.html"
    if _html331.exists():
        _hs331 = _html331.read_text(encoding="utf-8")
        _stripped331 = re.sub(r"<!--.*?-->", "", _hs331, flags=re.DOTALL)
        # 任意の attribute="javascript:..." を検出
        _js_urls331 = re.findall(
            r'\b[a-zA-Z-]+\s*=\s*"javascript:[^"]*"',
            _stripped331, flags=re.IGNORECASE)
        _count331 = len(_js_urls331)
        _ok331 = _count331 == 0
        check(
            _ok331,
            "Check 331: index.html attribute=\"javascript:...\" 0 件 (JS-URL-scheme 排除)",
            (f"Check 331: JS URL scheme 検出: {_js_urls331[:3]!r} — "
             "CSP script-src bypass、XSS 永続 vector。javascript: を削除し "
             "addEventListener + プログラム的遷移へ書き換えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 331: index.html present",
              "Check 331: index.html が無い", blocking=True)

    # ── 332. Root classic-script files have no import/export (BLOCKING) ──────────
    _root_classic332 = [
        ROOT / "aio-guard.js",
        ROOT / "theme-init.js",
        ROOT / "karte-init.js",
        ROOT / "error-suppressor.js",
    ]
    _bad_esm332: dict[str, list[str]] = {}
    _missing332: list[str] = []
    for _f in _root_classic332:
        if not _f.exists():
            _missing332.append(str(_f.relative_to(ROOT)))
            continue
        _src = _f.read_text(encoding="utf-8")
        # コメント行 (// および /* */) を strip
        _stripped = re.sub(r"//[^\n]*", "", _src)
        _stripped = re.sub(r"/\*.*?\*/", "", _stripped, flags=re.DOTALL)
        _lines = []
        for _kw in ("import", "export"):
            _hits = re.findall(rf"(?m)^\s*{_kw}\b", _stripped)
            if _hits:
                _lines.append(f"{_kw}={len(_hits)}")
        if _lines:
            _bad_esm332[str(_f.relative_to(ROOT))] = _lines
    _ok332 = (not _bad_esm332) and (not _missing332)
    check(
        _ok332,
        f"Check 332: root classic scripts {len(_root_classic332)} 件すべて ESM statement 0 (classic script contract)",
        (f"Check 332: root classic script に ESM statement: {_bad_esm332!r} / "
         f"missing files={_missing332!r} — <script type=\"module\"> でなく "
         "classic script として load されるので import/export は silent parse error。"
         "全 statement を script 内 local で完結させよ"),
        blocking=True,
    )

    # ── 333. webmanifest name/short_name/description real-name anonymity (BLOCKING) ─
    # PWA install prompt / app launcher は一般ユーザー向け UI 面ゆえ Check 124 と同じ
    # 匿名契約 (実名は AIO/entity 層のみ) を webmanifest にも強制。
    _webman333 = ROOT / "manifest.webmanifest"
    if _webman333.exists():
        try:
            _wm333 = json.loads(_webman333.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _wm333 = None
        if _wm333 is not None:
            _realnames333 = ("横井雄太", "Yokoi Yuta", "Yuta Yokoi")
            _leak333: list[str] = []
            for _field in ("name", "short_name", "description"):
                _v = str(_wm333.get(_field, ""))
                for _rn in _realnames333:
                    if _rn in _v:
                        _leak333.append(f"{_field} に {_rn!r}")
            _ok333 = not _leak333
            check(
                _ok333,
                "Check 333: webmanifest name/short_name/description に実名漏れ無し (PWA 匿名契約)",
                (f"Check 333: webmanifest に実名漏れ: {_leak333!r} — PWA install prompt / "
                 "app launcher は一般向け UI 面。実名は AIO/entity 層のみ (Check 124 と同契約)。"
                 "'yuta' 表記へ修正せよ"),
                blocking=True,
            )
        else:
            check(False, "Check 333: manifest.webmanifest parseable",
                  "Check 333: manifest.webmanifest が JSON parse 不能", blocking=True)
    else:
        check(False, "Check 333: manifest.webmanifest present",
              "Check 333: manifest.webmanifest が無い", blocking=True)

    # ── 334. webmanifest orientation in W3C enum (BLOCKING) ──────────────────────
    _webman334 = ROOT / "manifest.webmanifest"
    if _webman334.exists():
        try:
            _wm334 = json.loads(_webman334.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _wm334 = None
        if _wm334 is not None:
            _orient334 = str(_wm334.get("orientation", ""))
            _valid_orient334 = {
                "any", "natural", "landscape", "landscape-primary",
                "landscape-secondary", "portrait", "portrait-primary",
                "portrait-secondary",
            }
            # orientation は optional。存在する場合のみ enum 照合。
            _ok334 = (_orient334 == "") or (_orient334 in _valid_orient334)
            check(
                _ok334,
                f"Check 334: webmanifest orientation={_orient334!r} は W3C enum 内 (or 未設定)",
                (f"Check 334: webmanifest orientation={_orient334!r} が spec-invalid — "
                 f"allowed={sorted(_valid_orient334)}。typo は UA が無視し platform default "
                 "へ silent fallback。正規の値へ修正せよ"),
                blocking=True,
            )
        else:
            check(False, "Check 334: manifest.webmanifest parseable",
                  "Check 334: manifest.webmanifest が JSON parse 不能", blocking=True)
    else:
        check(False, "Check 334: manifest.webmanifest present",
              "Check 334: manifest.webmanifest が無い", blocking=True)

    # ── 335. index.html <link rel="manifest"> resolves to webmanifest (BLOCKING) ─
    _html335 = ROOT / "index.html"
    if _html335.exists():
        _hs335 = _html335.read_text(encoding="utf-8")
        _stripped335 = re.sub(r"<!--.*?-->", "", _hs335, flags=re.DOTALL)
        _m335 = re.search(
            r'<link\s+[^>]*rel="manifest"[^>]*>', _stripped335)
        _href335 = None
        if _m335:
            _mh = re.search(r'href="([^"]+)"', _m335.group(0))
            if _mh:
                _href335 = _mh.group(1)
        _resolved335 = None
        if _href335:
            # canonical prefix (/portfolio/) と ./ を剥がして repo-relative へ正規化
            _rel335 = _href335
            for _pfx in ("https://yutapr0117-design.github.io/portfolio/",
                         "/portfolio/", "./", "/"):
                if _rel335.startswith(_pfx):
                    _rel335 = _rel335[len(_pfx):]
                    break
            _resolved335 = ROOT / _rel335
        _ok335 = (_href335 is not None
                  and _resolved335 is not None
                  and _resolved335.is_file())
        check(
            _ok335,
            f"Check 335: <link rel=\"manifest\"> href={_href335!r} が実 webmanifest file に解決",
            (f"Check 335: <link rel=\"manifest\"> "
             f"{'不在' if _href335 is None else f'href={_href335!r} が file 解決しない'} — "
             "PWA install capability が全 gate に silent で無効化 (install prompt / "
             "home-screen icon / standalone 起動 喪失)。link tag と href を復元せよ"),
            blocking=True,
        )
    else:
        check(False, "Check 335: index.html present",
              "Check 335: index.html が無い", blocking=True)

    # ── 336. og:image == twitter:image byte-identical (BLOCKING) ─────────────────
    _html336 = ROOT / "index.html"
    if _html336.exists():
        _hs336 = _html336.read_text(encoding="utf-8")
        _stripped336 = re.sub(r"<!--.*?-->", "", _hs336, flags=re.DOTALL)
        _og336 = re.search(
            r'<meta\s+property="og:image"\s+content="([^"]+)"', _stripped336)
        _tw336 = re.search(
            r'<meta\s+name="twitter:image"\s+content="([^"]+)"', _stripped336)
        _og_v336 = _og336.group(1) if _og336 else None
        _tw_v336 = _tw336.group(1) if _tw336 else None
        _ok336 = (_og_v336 is not None
                  and _tw_v336 is not None
                  and _og_v336 == _tw_v336)
        check(
            _ok336,
            f"Check 336: og:image == twitter:image (byte-identical single social-card image)",
            (f"Check 336: og:image / twitter:image drift: "
             f"og:image={_og_v336!r} != twitter:image={_tw_v336!r} — "
             "Twitter card と OG (LinkedIn/Slack/FB) が別 image を表示し entity "
             "visual identity が SNS ごとに分裂。単一 canonical image へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 336: index.html present",
              "Check 336: index.html が無い", blocking=True)

    # ── 337. Canonical binary assets magic-byte format integrity (BLOCKING) ──────
    _webp337 = ROOT / "yuta-yokoi-ai-pm-orchestration-system.webp"
    _mp3_337 = ROOT / "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3"
    _fmt_problems337: list[str] = []
    if _webp337.is_file():
        _wh337 = _webp337.read_bytes()[:12]
        if not (_wh337[0:4] == b"RIFF" and _wh337[8:12] == b"WEBP"):
            _fmt_problems337.append(
                f"{_webp337.name} が WebP magic bytes (RIFF....WEBP) を持たない: "
                f"head={_wh337[:12]!r}")
    else:
        _fmt_problems337.append(f"{_webp337.name} が存在しない")
    if _mp3_337.is_file():
        _mh337 = _mp3_337.read_bytes()[:3]
        _is_id3 = _mh337[0:3] == b"ID3"
        _is_frame_sync = (len(_mh337) >= 2 and _mh337[0] == 0xFF
                          and (_mh337[1] & 0xE0) == 0xE0)
        if not (_is_id3 or _is_frame_sync):
            _fmt_problems337.append(
                f"{_mp3_337.name} が MP3 magic bytes (ID3 or frame-sync 0xFFEx) を持たない: "
                f"head={_mh337!r}")
    else:
        _fmt_problems337.append(f"{_mp3_337.name} が存在しない")
    check(
        not _fmt_problems337,
        "Check 337: canonical binary assets (hero.webp / BGM.mp3) の magic bytes が拡張子と一致",
        (f"Check 337: binary asset format-integrity 違反: {_fmt_problems337!r} — "
         "拡張子は保ったまま中身が別 format に差し替わると Check 269 (byte budget) を "
         "通過するが content-type sniff する crawler/browser が reject/mis-render。"
         "正規 format のファイルへ差し戻せ"),
        blocking=True,
    )
