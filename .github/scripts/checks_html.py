"""
checks_html.py — index.html document/meta baseline & lang coherence checks (glob-content: html)
(extracted from check_repository_consistency.py — check.py split track・category "HTML baseline"・ctx-enrich module).

Non-contiguous cluster of Checks 8/20/115/152/187/220/250/255/303/306 that read the pre-loaded
index.html content (the monolith's `html` global, attached as `_ctx.html`). Themes: security meta
(8 nosniff / 115 CSP hardening baseline), og:image dims (20), <html lang> ↔ inLanguage / og:locale /
manifest.lang coherence + BCP-47 validity (152/187/220/250), document structure (255 DOCTYPE / 306
closing tag), and root data-attributes (303). Check 7 (CSP-before-suppressor) is NOT included: it
depends on the _lib_io.csp_sri_hash helper (a separate helper-consolidation task). No other
cross-section var coupling.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/html/read/extract by reference (exec 不使用).

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  8.  index.html has no <meta http-equiv="X-Content-Type-Options"> (header-only control)
  20. index.html has og:image:width / og:image:height / og:image:alt
  115. index.html CSP hardening baseline: the Content-Security-Policy meta must NOT contain
       `'unsafe-inline'` or `'unsafe-eval'` (which would defeat the XSS protection — the site
       authorizes inline scripts/handlers via sha256 hashes + `'unsafe-hashes'`, not blanket
       unsafe-inline), AND must retain `default-src 'self'`, `object-src 'none'`, `base-uri
       'self'`, the Trusted Types pair `require-trusted-types-for 'script'` and
       `trusted-types default`, plus `form-action 'none'` (no HTML forms exist; blocks form
       exfiltration) and `upgrade-insecure-requests` (blocks HTTP downgrade / mixed content) —
       both have zero legitimate-removal scenario so they belong in the anti-weakening baseline.
       The Trusted Types directives pair with main.js's
       `trustedTypes.createPolicy('default')` (Check 43c): dropping require-trusted-types-for
       un-enforces the innerHTML interceptor's fail-closed XSS block, and removing 'default' from
       trusted-types makes createPolicy('default') CSP-blocked (app fails to boot). Guards against
       silent CSP weakening (a high-impact security regression class, the runtime-policy
       counterpart of Check 7's position/hash checks). (BLOCKING)
  152. `<html lang>` ↔ JSON-LD `inLanguage` coherence: the index.html `<html lang>` attribute and
       every JSON-LD `"inLanguage": "..."` declaration across index.html, main.js, and
       js/meta-management.js must declare the same language code. Drift is SILENT — AI/SEO crawlers
       see conflicting language signals (e.g. `<html lang="ja">` but JSON-LD `inLanguage: "en"`)
       and may misclassify the content's primary language, degrading discovery in language-scoped
       search and AIO. This Check collects all values into a single set and asserts cardinality 1
       (single canonical language), with `<html lang>` present and at least one JSON-LD inLanguage
       declaration found. (BLOCKING)
  187. `<meta property="og:locale">` language code matches `<html lang>`: the
       language sub-tag of og:locale (e.g. `ja_JP` → `ja`) must equal the
       `<html lang>` attribute (e.g. `ja`). Drift would silently send conflicting
       language signals to social/OG crawlers (LinkedIn/Slack/Facebook unfurl) vs
       browsers and SEO crawlers — preview cards would localize to a different
       audience than the page itself. Sibling of Check 152 (lang ↔ JSON-LD
       inLanguage) for the og:locale surface. (BLOCKING)
  220. manifest.webmanifest `lang` matches HTML `<html lang>`: the PWA
       manifest's `lang` field MUST equal the index.html `<html lang>`
       attribute (e.g. both `ja`). Drift would silently make the installed
       PWA report a different language than the rendered HTML — screen
       readers, OS-level language selectors, and AI/SEO consumers see
       conflicting language signals. Sibling of Check 152 (<html lang> ↔
       JSON-LD inLanguage) / Check 187 (og:locale ↔ <html lang>) for the
       manifest install layer. (BLOCKING)

  250. `<html lang>` value is valid BCP-47 tag: the index.html `<html
       lang="...">` attribute MUST match BCP-47 regex
       `^[a-zA-Z]{2,3}(?:-[a-zA-Z0-9]{1,8})*$`. Drift (e.g. `jp` non-spec
       2-letter / `JAPANESE` ALL-CAPS word / `ja_JP` underscore) silently
       breaks browser language selection, screen-reader voice, AI/SEO
       language signal. Check 152/187/220 enforce inter-surface equality;
       Check 250 enforces BCP-47 syntactic validity of the canonical
       source value. (BLOCKING)

  255. index.html starts with `<!DOCTYPE html>` (HTML5 declaration):
       the index.html file MUST start with `<!DOCTYPE html>` (case-
       insensitive, ignoring leading BOM/whitespace). Drift silently
       triggers browser quirks mode — CSS box model regression, line-
       height drift, layout breakage. Sibling of Check 157 (head meta
       baseline) for the document-mode declaration axis. (BLOCKING)

  303. `<html data-theme>` == "system" AND `<html data-brand>` in
       {"indigo", "classic"}: index.html `<html>` initial data-theme +
       data-brand attribute values MUST match canonical starter values.
       Drift silently changes FOUC-prevention initial paint / brand
       fallback. Sibling of Check 302 for the html root attribute axis.
       (BLOCKING)

  306. index.html ends with closing `</html>` tag: the last non-empty
       line of index.html MUST be `</html>` (trailing whitespace/newline
       allowed). Drift = truncated HTML from Edit failure / build error
       silently ships incomplete markup. Sibling of Check 255 (DOCTYPE
       opening) for the HTML structural-closure axis. (BLOCKING)

"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    html = ctx.html
    read = ctx.read
    extract = ctx.extract

    # ── 8. No X-Content-Type-Options meta ────────────────────────────────────────
    check(
        '<meta http-equiv="X-Content-Type-Options"' not in html,
        "index.html: no X-Content-Type-Options meta (header-only control)",
        "index.html: X-Content-Type-Options meta present (must be removed; it's a header-only control)",
    )

    # ── 20. og:image:width / og:image:height / og:image:alt present ──────────────
    check(
        'property="og:image:width"' in html,
        "index.html: og:image:width present",
        "index.html: og:image:width missing (add <meta property=og:image:width>)",
    )
    check(
        'property="og:image:height"' in html,
        "index.html: og:image:height present",
        "index.html: og:image:height missing (add <meta property=og:image:height>)",
    )
    check(
        'property="og:image:alt"' in html,
        "index.html: og:image:alt present",
        "index.html: og:image:alt missing (add <meta property=og:image:alt>)",
    )

    # ── 115. index.html CSP hardening baseline (BLOCKING) ─────────────────────────
    # CSP の弱体化 (script-src への 'unsafe-inline'/'unsafe-eval' 混入や必須 directive の欠落) は XSS
    # 防御を無効化する高影響のセキュリティ退行。本サイトは inline を sha256 hash + 'unsafe-hashes' で
    # 許可しており blanket 'unsafe-inline' は使わない。CSP meta の content を抽出し、危険トークン不在 +
    # 必須 directive 存在を BLOCKING で機械強制する (Check 7 の position/hash に対する runtime-policy 面)。
    # 必須 directive には Trusted Types の 2 つ (require-trusted-types-for 'script' / trusted-types default)
    # を含む: これらは main.js の trustedTypes.createPolicy('default') (Check 43c が存在を強制) と「対に
    # なって機能する」security 不変条件で、(a) require-trusted-types-for が消えると innerHTML interceptor の
    # fail-closed 保護がブラウザ非強制化して XSS 防御が弱体化し、(b) trusted-types の許可名から 'default' が
    # 外れると createPolicy('default') が CSP にブロックされ app 自体が起動失敗する。main.js 側 (43c) のみ
    # 強制し CSP 側を放置すると pairing が片肺になるため、ここで CSP 側も BLOCKING で固定する。
    # さらに form-action 'none' (本サイトに HTML form は無く明示ブロック=フォーム exfiltration 遮断) と
    # upgrade-insecure-requests (HTTP downgrade / mixed-content 遮断) も必須化する: いずれも除去が常に
    # security weakening でゼロ legitimate-removal シナリオのため anti-weakening baseline に含める。
    _csp_m115 = re.search(r'http-equiv="Content-Security-Policy"\s+content="(.*?)"', html, re.DOTALL)
    if _csp_m115:
        _csp115 = _csp_m115.group(1)
        _problems115 = []
        if "'unsafe-inline'" in _csp115:
            _problems115.append("'unsafe-inline' が存在 (XSS 防御を無効化)")
        if "'unsafe-eval'" in _csp115:
            _problems115.append("'unsafe-eval' が存在")
        for _req115 in [
            "default-src 'self'", "object-src 'none'", "base-uri 'self'",
            "require-trusted-types-for 'script'", "trusted-types default",
            "form-action 'none'", "upgrade-insecure-requests",
        ]:
            if _req115 not in _csp115:
                _problems115.append(f"必須 directive 欠落: {_req115}")
        check(
            not _problems115,
            "Check 115: index.html CSP がセキュリティ baseline を維持 (unsafe-inline/eval 無し + 必須 directive 存在)",
            f"Check 115: CSP 弱体化を検出: {_problems115} — XSS 防御 baseline を復元せよ",
            blocking=True,
        )
    else:
        check(False, "", "Check 115: index.html に Content-Security-Policy meta が見つからない — CSP baseline を検証できない", blocking=True)

    # ── 152. <html lang> ↔ JSON-LD inLanguage coherence (BLOCKING) ─────────────────
    # index.html `<html lang>` 属性と全 JSON-LD `inLanguage` 宣言 (index.html / main.js /
    # js/meta-management.js) が同一の言語コードであることを BLOCKING 強制する。drift は
    # SILENT — AI/SEO crawler が conflicting な言語 signal を見て primary language を
    # 誤分類し、言語スコープ検索 (Google "site:" lang filter / AI search) と AIO で
    # discovery が劣化する。本 Check は全 surface から値を集めて単一集合の cardinality
    # が 1 であることを検証 (canonical 言語が一つに保たれる)。
    _idx152 = ROOT / "index.html"
    _main152 = ROOT / "main.js"
    _meta152 = ROOT / "js" / "meta-management.js"
    if _idx152.exists() and _main152.exists() and _meta152.exists():
        _isrc152 = _idx152.read_text(encoding="utf-8")
        _msrc152 = _main152.read_text(encoding="utf-8")
        _mtsrc152 = _meta152.read_text(encoding="utf-8")
        _html_lang152_m = re.search(
            r'<html[^>]+\blang\s*=\s*["\']([a-zA-Z][\w-]*)["\']', _isrc152
        )
        _html_lang152 = _html_lang152_m.group(1) if _html_lang152_m else None
        _in_lang152: list[tuple[str, str]] = []  # (where, value)
        for _src152, _label152 in [
            (_isrc152, "index.html"),
            (_msrc152, "main.js"),
            (_mtsrc152, "js/meta-management.js"),
        ]:
            for _val152 in re.findall(
                r"['\"]inLanguage['\"]\s*:\s*['\"]([a-zA-Z][\w-]*)['\"]", _src152
            ):
                _in_lang152.append((_label152, _val152))
        _all_lang152: set[str] = {v for (_, v) in _in_lang152}
        if _html_lang152:
            _all_lang152.add(_html_lang152)
        _ok152 = (
            _html_lang152 is not None
            and len(_in_lang152) > 0
            and len(_all_lang152) == 1
        )
        check(
            _ok152,
            f"Check 152: <html lang>={_html_lang152!r} と {len(_in_lang152)} 件の "
            f"JSON-LD inLanguage が全て {_all_lang152} で一致",
            (f"Check 152: 言語コード drift: <html lang>={_html_lang152!r} / "
             f"JSON-LD inLanguage={_in_lang152} / 全集合={_all_lang152}。AI/SEO crawler "
             "が conflicting 言語 signal で primary language を誤分類する。index.html "
             "<html lang> と全 JSON-LD inLanguage を同一言語コードへ統一せよ"
             if _html_lang152 and _in_lang152 else
             f"Check 152: 言語宣言を抽出できない (<html lang>={_html_lang152} / "
             f"inLanguage 件数={len(_in_lang152)}) — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 152: index.html + main.js + js/meta-management.js present",
              "Check 152: 言語 coherence 検証に必要な 3 source のいずれかが無い", blocking=True)

    # ── 187. og:locale language sub-tag matches <html lang> (BLOCKING) ────────────
    # index.html `<meta property="og:locale">` の language sub-tag (例 ja_JP → ja)
    # が `<html lang>` 属性 (例 ja) と一致することを BLOCKING 強制。drift は SILENT に
    # OG crawler (LinkedIn/Slack/Facebook unfurl) と browser/SEO crawler へ別言語
    # signal を送り、preview card が page と別の audience へ localize される。
    # Check 152 (lang ↔ JSON-LD inLanguage) の og:locale 軸版。
    _idx187 = ROOT / "index.html"
    if _idx187.exists():
        _isrc187 = _idx187.read_text(encoding="utf-8")
        _lang187_m = re.search(r'<html\s+[^>]*lang=["\']([^"\']+)["\']', _isrc187)
        _ogl187_m = re.search(
            r'<meta\s+property=["\']og:locale["\']\s+content=["\']([^"\']+)["\']', _isrc187
        )
        _lang187 = _lang187_m.group(1) if _lang187_m else None
        _ogl187 = _ogl187_m.group(1) if _ogl187_m else None
        # og:locale の language sub-tag (underscore 区切りの先頭)
        _ogl_lang187 = _ogl187.split("_")[0] if _ogl187 else None
        _ok187 = (
            _lang187 is not None
            and _ogl_lang187 is not None
            and _lang187 == _ogl_lang187
        )
        check(
            _ok187,
            f"Check 187: og:locale={_ogl187!r} (lang={_ogl_lang187!r}) == <html lang>={_lang187!r}",
            (f"Check 187: og:locale language drift: og:locale={_ogl187!r} (lang={_ogl_lang187!r}) / "
             f"<html lang>={_lang187!r} — OG crawler が page と別 audience へ localize。"
             "og:locale の language sub-tag を <html lang> と揃えよ"
             if _lang187 and _ogl187 else
             f"Check 187: og:locale / <html lang> 抽出不可 "
             f"(og:locale={_ogl187} / html lang={_lang187})"),
            blocking=True,
        )
    else:
        check(False, "Check 187: index.html present",
              "Check 187: index.html が無い", blocking=True)

    # ── 220. manifest.webmanifest lang == <html lang> (BLOCKING) ──────────────────
    # manifest.webmanifest `lang` field と index.html `<html lang>` attribute が
    # strict 一致することを BLOCKING 強制。drift は SILENT に PWA install で OS/screen
    # reader/AI/SEO consumer に異なる言語信号を流す。Check 152 (<html lang> ↔
    # JSON-LD inLanguage) / Check 187 (og:locale ↔ <html lang>) の manifest install 軸版。
    _idx220 = ROOT / "index.html"
    _mani220 = ROOT / "manifest.webmanifest"
    if _idx220.exists() and _mani220.exists():
        _isrc220 = _idx220.read_text(encoding="utf-8")
        _html_lang220_m = re.search(r'<html\s+lang=["\']([^"\']+)["\']', _isrc220)
        _html_lang220 = _html_lang220_m.group(1) if _html_lang220_m else None
        try:
            _mdata220 = json.loads(_mani220.read_text(encoding="utf-8"))
        except json.JSONDecodeError as _e220:
            _mdata220 = None
        _mani_lang220 = _mdata220.get("lang") if isinstance(_mdata220, dict) else None
        _ok220 = (
            _html_lang220 is not None
            and _mani_lang220 is not None
            and _html_lang220 == _mani_lang220
        )
        check(
            _ok220,
            f"Check 220: manifest.lang={_mani_lang220!r} == <html lang>={_html_lang220!r}",
            (f"Check 220: language drift: manifest.lang={_mani_lang220!r}, "
             f"<html lang>={_html_lang220!r} — PWA install と HTML render で言語信号が "
             "split。manifest.lang を <html lang> と同一値へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 220: index.html + manifest.webmanifest present",
              "Check 220: index.html もしくは manifest.webmanifest が無い", blocking=True)

    # ── 250. <html lang> value is BCP-47 valid (BLOCKING) ─────────────────────────
    # index.html `<html lang="...">` 値が BCP-47 regex に一致することを BLOCKING 強制。
    # Check 152/187/220 (inter-surface 一致) を補完する syntactic 軸。
    _idx250 = ROOT / "index.html"
    if _idx250.exists():
        _isrc250 = _idx250.read_text(encoding="utf-8")
        _hl250_m = re.search(r'<html\s+lang=["\']([^"\']+)["\']', _isrc250)
        _hl250 = _hl250_m.group(1) if _hl250_m else None
        _bcp47_re250 = re.compile(r"^[a-zA-Z]{2,3}(?:-[a-zA-Z0-9]{1,8})*$")
        _ok250 = isinstance(_hl250, str) and bool(_bcp47_re250.match(_hl250))
        check(
            _ok250,
            f"Check 250: <html lang>={_hl250!r} is BCP-47 valid",
            (f"Check 250: <html lang>={_hl250!r} 非 BCP-47 — browser 言語選択 / screen reader / "
             "AI/SEO 言語信号 silent 破壊。BCP-47 (例 'ja' / 'ja-JP' / 'en-US') へ訂正"),
            blocking=True,
        )
    else:
        check(False, "Check 250: index.html present",
              "Check 250: index.html が無い", blocking=True)

    # ── 255. index.html starts with <!DOCTYPE html> (HTML5 declaration) (BLOCKING) ─
    # index.html が `<!DOCTYPE html>` (case-insensitive, leading BOM/whitespace 無視)
    # で始まることを BLOCKING 強制。drift で browser quirks mode 発火 → CSS box model
    # 退行 / line-height drift / layout 破壊。Check 157 の document-mode declaration 軸。
    _idx255 = ROOT / "index.html"
    if _idx255.exists():
        _isrc255 = _idx255.read_text(encoding="utf-8")
        _head255 = _isrc255.lstrip("﻿").lstrip()
        _ok255 = bool(re.match(r"<!DOCTYPE\s+html\s*>", _head255, re.IGNORECASE))
        check(
            _ok255,
            "Check 255: index.html starts with <!DOCTYPE html> (HTML5)",
            ("Check 255: index.html が <!DOCTYPE html> で始まらない — browser quirks "
             "mode 発火で CSS box model 退行・layout 破壊。先頭に <!DOCTYPE html> を配置"),
            blocking=True,
        )
    else:
        check(False, "Check 255: index.html present",
              "Check 255: index.html が無い", blocking=True)

    # ── 303. <html data-theme=system> AND <html data-brand> valid (BLOCKING) ──────
    # index.html `<html>` の initial data-theme == "system" かつ data-brand ∈
    # {"indigo","classic"} を BLOCKING 強制。Check 302 の html root attribute 軸版。
    _VALID_BRANDS303 = {"indigo", "classic"}
    _idx303 = ROOT / "index.html"
    if _idx303.exists():
        _isrc303 = _idx303.read_text(encoding="utf-8")
        _html_tag303_m = re.search(r"<html\s+([^>]+)>", _isrc303)
        _dt303 = None
        _db303 = None
        if _html_tag303_m:
            _attrs = _html_tag303_m.group(1)
            _dt_m = re.search(r'data-theme=["\']([^"\']+)["\']', _attrs)
            _db_m = re.search(r'data-brand=["\']([^"\']+)["\']', _attrs)
            _dt303 = _dt_m.group(1) if _dt_m else None
            _db303 = _db_m.group(1) if _db_m else None
        _bad303: list[str] = []
        if _dt303 != "system":
            _bad303.append(f"data-theme={_dt303!r} != 'system'")
        if _db303 not in _VALID_BRANDS303:
            _bad303.append(f"data-brand={_db303!r} not in {sorted(_VALID_BRANDS303)!r}")
        _ok303 = not _bad303
        check(
            _ok303,
            f"Check 303: <html data-theme>={_dt303!r} + data-brand={_db303!r} match canonical initial values",
            (f"Check 303: 違反: {_bad303!r} — FOUC-prevention initial paint / brand "
             "fallback が canonical initial values から drift"),
            blocking=True,
        )
    else:
        check(False, "Check 303: index.html present",
              "Check 303: index.html が無い", blocking=True)

    # ── 306. index.html ends with </html> (BLOCKING) ──────────────────────────────
    # index.html の trailing 空白行を除いた最終行が `</html>` で終わることを BLOCKING
    # 強制。Check 255 (DOCTYPE opening) の structural-closure 軸版。
    _idx306 = ROOT / "index.html"
    if _idx306.exists():
        _isrc306 = _idx306.read_text(encoding="utf-8")
        _rstripped306 = _isrc306.rstrip()
        _ok306 = _rstripped306.endswith("</html>")
        check(
            _ok306,
            "Check 306: index.html ends with </html>",
            (f"Check 306: index.html 末尾が </html> でない (last 30 chars={_rstripped306[-30:]!r}) — "
             "truncated HTML / build error suspect"),
            blocking=True,
        )
    else:
        check(False, "Check 306: index.html present",
              "Check 306: index.html が無い", blocking=True)
