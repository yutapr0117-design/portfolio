"""
checks_csp_security.py — shipped-JS security + CSP script authorization checks — sitemap loc / innerHTML fail-closed / DOMParser absence / script-src+connect-src host authz (351-355)
(extracted from check_repository_consistency.py — check.py split track).

run(ctx) receives shared check()/ROOT by reference (exec 不使用) so exit code / BLOCKING propagation
are byte-equivalent. annotation+def-aware free-var 分析で外部 `_`-var・global-content 依存ゼロ確認済。
nested-fn の module-level `global _accNNN` は run() 内で `nonlocal` へ機械変換 (意味等価)。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  351. EVERY `<url>` block in sitemap.xml MUST contain EXACTLY ONE `<loc>`
       element. `<loc>` is required by the sitemaps.org schema; a `<url>`
       block missing it is invalid and crawlers silently drop that entry
       (the URL disappears from discovery), while a block with two `<loc>`
       is undefined behavior. Check 312 guards `<loc>` uniqueness ACROSS
       blocks (no duplicate URLs); this guards the per-block cardinality
       (each block has one). Sibling of Check 312 (loc uniqueness) /
       Check 307 (sitemap XML structure) for the sitemap url-block
       structural-completeness axis. (BLOCKING)

  352. `js/ui-components.js` `h()` (the single DOM builder used by every
       render path) MUST retain its fail-closed innerHTML prohibition:
       the `html` attribute key branch MUST `throw` (not assign
       `el.innerHTML`). `h()` is the architectural XSS boundary — all
       user/state text flows through it as `createTextNode`. If the throw
       is replaced by an `el.innerHTML = value` assignment, every call
       site that passes an `html` attr becomes an XSS sink and the entire
       no-innerHTML contract (Boring Technology + Trusted Types) collapses
       silently. Sibling of Check 239 (no eval) / Check 43 (protected
       blocks) for the shipped-JS XSS-boundary integrity axis. (BLOCKING)

  353. `js/ui-components.js` MUST NOT contain actual `DOMParser` usage
       (only comments documenting its removal are allowed). `createIcon()`
       builds SVG via `createElementNS` + static regex attribute
       extraction precisely to avoid `DOMParser.parseFromString`, which
       invokes the Trusted Types `createHTML` handler and violates the
       `require-trusted-types-for 'script'` CSP (Check 43c/115). Drift =
       reverting createIcon to DOMParser re-introduces the Trusted Types
       violation silently (icons still render, so behavior e2e stays
       green). Note: main.js legitimately uses DOMParser inside its
       protected innerHTML-interceptor sanitizer, so this Check is scoped
       to ui-components.js only. Sibling of Check 352 (h innerHTML) /
       Check 43c (Trusted Types) for the createIcon Trusted-Types-boundary
       axis. (BLOCKING)

  354. Every external `<script src="https://...">` host in index.html
       (currently the KARTE `cdn-edge.karte.io` analytics loader) MUST
       appear in the CSP `script-src` directive. This machine-enforces the
       C7 contract ("KARTE gets no SRI; its connection is restricted by
       CSP instead"). Drift = the KARTE host is dropped from `script-src`
       (or the loader URL host changes) while the `<script>` tag remains,
       so Chrome CSP-blocks the loader — analytics silently dies (the
       queue-stub buffers forever) with only a console error that no
       behavior e2e observes. Sibling of Check 63 (crawler origin
       alignment) / Check 115 (CSP baseline) for the external-script
       CSP-authorization axis. (BLOCKING)

  355. Every external `<script src="https://...">` host in index.html MUST
       ALSO appear in the CSP `connect-src` directive. The analytics
       loader (KARTE edge.js) fetches its runtime config and beacons from
       its own origin; being authorized to LOAD (script-src, Check 354)
       but not to CONNECT (connect-src) means the script loads yet all its
       XHR/fetch calls are CSP-blocked — analytics half-breaks silently
       (config never fetched, events never sent). Check 354 covers the
       load leg; this covers the connect leg. Sibling of Check 354
       (script-src authorization) for the external-script
       connect-authorization axis. (BLOCKING)

"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 351. Every sitemap <url> block has exactly one <loc> (BLOCKING) ──────────
    _sitemap351 = ROOT / "sitemap.xml"
    if _sitemap351.is_file():
        _sm351 = _sitemap351.read_text(encoding="utf-8")
        _url_blocks351 = re.findall(r"<url>.*?</url>", _sm351, re.DOTALL)
        _bad351: list[str] = []
        for _i, _blk in enumerate(_url_blocks351):
            _loc_count = _blk.count("<loc>")
            if _loc_count != 1:
                _m = re.search(r"<loc>([^<]*)</loc>", _blk)
                _hint = _m.group(1) if _m else "(loc 無し)"
                _bad351.append(f"url[{_i}] loc={_loc_count} 個 ({_hint})")
        _ok351 = (not _bad351) and len(_url_blocks351) > 0
        check(
            _ok351,
            f"Check 351: sitemap.xml の全 <url> block ({len(_url_blocks351)} 件) が <loc> を厳密 1 個持つ",
            (f"Check 351: <url> block の loc cardinality 違反: {_bad351!r} — "
             "loc は sitemap 仕様の必須要素。欠落 block は crawler に silent drop され "
             "discovery から消える / 複数 loc は undefined behavior。各 block に loc 1 個へ修正せよ"),
            blocking=True,
        )
    else:
        check(False, "Check 351: sitemap.xml present",
              "Check 351: sitemap.xml が無い", blocking=True)

    # ── 352. h() retains fail-closed innerHTML prohibition (BLOCKING) ────────────
    # h() は全 render 経路が使う単一 DOM builder = アーキテクチャの XSS 境界。
    # 'html' attr key branch が throw であること (el.innerHTML 代入でないこと) を強制。
    _uic352 = ROOT / "js" / "ui-components.js"
    if _uic352.is_file():
        _usrc352 = _uic352.read_text(encoding="utf-8")
        _problems352: list[str] = []
        # (a) innerHTML prohibition throw が存在する
        if "innerHTML is strictly prohibited" not in _usrc352:
            _problems352.append("innerHTML-prohibition throw が消えている")
        # (b) el.innerHTML への代入が存在しない (XSS sink 化の直接兆候)
        if re.search(r"\.innerHTML\s*=", _usrc352):
            _problems352.append(".innerHTML = 代入が存在 (XSS sink)")
        _ok352 = not _problems352
        check(
            _ok352,
            "Check 352: js/ui-components.js h() が fail-closed innerHTML 禁止 (throw 保持 + .innerHTML= 代入なし)",
            (f"Check 352: XSS 境界 drift: {_problems352!r} — "
             "h() の 'html' key branch が throw でなくなる or .innerHTML= 代入が入ると "
             "全 h() call site が XSS sink 化し no-innerHTML 契約 (Trusted Types) が崩壊。"
             "throw new Error('[h] innerHTML is strictly prohibited...') を復元せよ"),
            blocking=True,
        )
    else:
        check(False, "Check 352: js/ui-components.js present",
              "Check 352: js/ui-components.js が無い", blocking=True)

    # ── 353. js/ui-components.js has no actual DOMParser usage (BLOCKING) ────────
    # createIcon() は createElementNS + regex で SVG を組み Trusted Types 適合を保つ。
    # DOMParser 復活は TT 違反を silent 再導入 (icon は描画され behavior e2e 緑のまま)。
    # main.js は innerHTML-interceptor sanitizer で DOMParser を正当使用ゆえ scope 外。
    _uic353 = ROOT / "js" / "ui-components.js"
    if _uic353.is_file():
        _usrc353 = _uic353.read_text(encoding="utf-8")
        # コメント (// と /* */) を除去してから実コードの DOMParser を検出
        _code353 = re.sub(r"/\*.*?\*/", "", _usrc353, flags=re.DOTALL)
        _code353 = re.sub(r"//[^\n]*", "", _code353)
        _domparser353 = re.findall(r"\bDOMParser\b", _code353)
        _ok353 = not _domparser353
        check(
            _ok353,
            "Check 353: js/ui-components.js 実コードに DOMParser 不在 (createIcon Trusted Types 適合)",
            (f"Check 353: js/ui-components.js 実コードに DOMParser 使用 ({len(_domparser353)} 件) — "
             "createIcon が DOMParser.parseFromString に戻ると Trusted Types createHTML handler を "
             "呼び require-trusted-types-for 'script' CSP (Check 43c/115) 違反を silent 再導入。"
             "createElementNS + regex 抽出へ戻せ"),
            blocking=True,
        )
    else:
        check(False, "Check 353: js/ui-components.js present",
              "Check 353: js/ui-components.js が無い", blocking=True)

    # ── 354. external <script src> hosts are authorized in CSP script-src (BLOCKING) ─
    # C7 契約 (KARTE は SRI 無し・CSP で接続制限) を機械強制。外部 script host が
    # script-src から消えると Chrome が loader を CSP-block し analytics が silent 死。
    _idx354 = ROOT / "index.html"
    if _idx354.is_file():
        _h354 = _idx354.read_text(encoding="utf-8")
        _h354_nc = re.sub(r"<!--.*?-->", "", _h354, flags=re.DOTALL)
        # CSP script-src directive を抽出 (content は double-quote 内・値に single quote を含む)
        _csp_m354 = re.search(r'Content-Security-Policy"\s+content="([^"]*)"',
                              _h354_nc, re.DOTALL)
        _script_src354 = ""
        if _csp_m354:
            for _d in _csp_m354.group(1).split(";"):
                if _d.strip().startswith("script-src"):
                    _script_src354 = _d
                    break
        # 外部 <script src="https://host/..."> の host を全抽出
        _ext_hosts354 = set(re.findall(
            r'<script[^>]*\ssrc="https://([^/"]+)', _h354_nc))
        _unauthorized354 = sorted(
            _host for _host in _ext_hosts354
            if f"https://{_host}" not in _script_src354)
        _ok354 = (not _unauthorized354) and bool(_script_src354)
        check(
            _ok354,
            f"Check 354: 外部 script host {sorted(_ext_hosts354)} すべて CSP script-src で authorize",
            (f"Check 354: CSP script-src が外部 script host を authorize しない: {_unauthorized354!r} — "
             "C7 契約違反。KARTE 等の loader が Chrome に CSP-block され analytics が silent 死 "
             "(queue-stub が永久 buffer)。host を script-src へ追加せよ"
             if _script_src354 else
             "Check 354: CSP script-src directive が見つからない"),
            blocking=True,
        )
    else:
        check(False, "Check 354: index.html present",
              "Check 354: index.html が無い", blocking=True)

    # ── 355. external <script src> hosts authorized in CSP connect-src (BLOCKING) ─
    # 354 の twin: loader (KARTE edge.js) は自 origin から config を fetch/beacon する。
    # LOAD 許可 (script-src) でも CONNECT 不許可 (connect-src) だと通信が CSP-block され
    # analytics が半壊 (config 取得不能・event 未送信) の silent drift。
    _idx355 = ROOT / "index.html"
    if _idx355.is_file():
        _h355 = _idx355.read_text(encoding="utf-8")
        _h355_nc = re.sub(r"<!--.*?-->", "", _h355, flags=re.DOTALL)
        _csp_m355 = re.search(r'Content-Security-Policy"\s+content="([^"]*)"',
                              _h355_nc, re.DOTALL)
        _connect_src355 = ""
        if _csp_m355:
            for _d in _csp_m355.group(1).split(";"):
                if _d.strip().startswith("connect-src"):
                    _connect_src355 = _d
                    break
        _ext_hosts355 = set(re.findall(
            r'<script[^>]*\ssrc="https://([^/"]+)', _h355_nc))
        _unauthorized355 = sorted(
            _host for _host in _ext_hosts355
            if f"https://{_host}" not in _connect_src355)
        _ok355 = (not _unauthorized355) and bool(_connect_src355)
        check(
            _ok355,
            f"Check 355: 外部 script host {sorted(_ext_hosts355)} すべて CSP connect-src で authorize",
            (f"Check 355: CSP connect-src が外部 script host を authorize しない: {_unauthorized355!r} — "
             "loader は LOAD 許可 (script-src) でも CONNECT 不許可だと XHR/fetch が CSP-block され "
             "analytics 半壊 (config 取得不能・event 未送信)。host を connect-src へ追加せよ"
             if _connect_src355 else
             "Check 355: CSP connect-src directive が見つからない"),
            blocking=True,
        )
    else:
        check(False, "Check 355: index.html present",
              "Check 355: index.html が無い", blocking=True)
