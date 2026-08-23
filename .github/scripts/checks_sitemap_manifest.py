"""
checks_sitemap_manifest.py — sitemap & manifest format/validity coherence checks (311-320, 386-387)
(extracted from check_repository_consistency.py — check.py split track).

run(ctx) receives shared check()/ROOT by reference (exec 不使用) so exit code / BLOCKING propagation
are byte-equivalent. annotation+def-aware free-var 分析で外部 `_`-var・global-content 依存ゼロ確認済。
nested-fn の module-level `global _accNNN` は run() 内で `nonlocal` へ機械変換 (意味等価)。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  311. sitemap.xml `<lastmod>` values MUST all match strict `YYYY-MM-DD`
       format AND MUST NOT be in the future (relative to today, JST). Drift
       = malformed date silently accepted by permissive Google/Bing parsers
       but rejected by strict crawlers, or a future date manipulating
       crawl priority. Sibling of Check 208 (JSON-LD dates ISO-8601) /
       Check 273 (JSON-LD dates not future) / Check 243 (LAST_UPDATED not
       future) for the sitemap.xml `<lastmod>` axis. (BLOCKING)

  312. sitemap.xml `<loc>` URLs MUST be unique (no duplicate entries).
       Drift = accidental copy-paste yielding two `<url>` blocks for the
       same URL, which per sitemaps.org RFC is undefined behavior and
       many crawlers de-duplicate at the cost of losing whichever metadata
       (lastmod/priority) came second. Also masks structural mistakes
       (missing new entry that was intended). Sibling of Check 217
       (@graph @id uniqueness) for the sitemap.xml `<loc>` axis. (BLOCKING)

  313. aio-manifest.json `generated_at` + `last_metadata_update` MUST NOT
       be in the future (relative to today, JST). Drift = timezone-slip
       or manual edit yielding a future timestamp, which AI crawlers
       interpret as "content from the future" and either reject as
       untrusted or over-index (recency ranking corruption). Sibling of
       Check 243 (SITE_CONFIG.LAST_UPDATED not future) / Check 273
       (JSON-LD dates not future) / Check 311 (sitemap.xml <lastmod> not
       future) for the aio-manifest.json date axis. (BLOCKING)

  314. manifest.webmanifest `theme_color` MUST equal at least one
       `<meta name="theme-color">` content value in index.html. Drift =
       PWA install screen / OS status bar shows a different color than
       the in-browser address bar. Cross-surface coherence between the
       webmanifest (installed-app appearance) and the meta tag
       (in-browser appearance). Sibling of Check 304 (theme-color hex
       format) / Check 305 (light+dark media coverage) for the
       webmanifest ↔ meta cross-surface color-identity axis. (BLOCKING)

  315. manifest.webmanifest `display` MUST be in W3C spec enumeration:
       `{fullscreen, standalone, minimal-ui, browser}`. `background_color`
       MUST be a 6-digit hex color (`#RRGGBB`). Drift = a typo (e.g.
       `standlone`) silently degrades PWA install prompt to `browser`
       fallback (all "installed" UX signals lost); a malformed
       background_color triggers OS-default gray on the splash screen.
       Sibling of Check 304 (theme-color hex format) / Check 210
       (start_url/scope canonical) for the webmanifest structural
       correctness axis. (BLOCKING)

  316. manifest.webmanifest `icons[].purpose` tokens MUST all be in W3C
       spec enumeration `{any, maskable, monochrome}`, and `icons[].sizes`
       MUST match strict format `<W>x<H>` (positive integers) or `any`.
       Drift = a typo (e.g. `mask`) silently makes the icon unusable for
       adaptive-icon rendering (Android/ChromeOS home-screen falls back
       to a generic icon), and a malformed sizes value causes UAs to
       reject the icon entry. Sibling of Check 315 (display enum) /
       Check 212 (icons[].src canonical) for the webmanifest icons
       structural correctness axis. (BLOCKING)

  317. `.well-known/aio-manifest.json` every `sha256` field (in
       source_of_truth[], supporting_evidence[], observational_evidence[])
       MUST match strict `^[0-9a-f]{64}$` (lowercase, exactly 64 hex
       chars). Drift = truncated (63 chars) / uppercase / space-embedded
       digest silently accepted by permissive `sha256sum -c` variants but
       rejected by strict hash-verification tooling. Also masks the
       cause when a Check like Check 42 (aio-manifest digest chain) fails
       — is it wrong content or wrong format? Sibling of Check 42 (digest
       chain) / Check 236 (generated_at RFC 3339) for the aio-manifest
       digest-field structural correctness axis. (BLOCKING)

  318. `.well-known/aio-manifest.json` every evidence entry (in
       source_of_truth[], supporting_evidence[], observational_evidence[])
       MUST have all three required fields `{path, role, sha256}` present
       AND non-empty. Drift = a missing `role` yields silent "unlabeled
       evidence" (AI crawler cannot interpret purpose); a missing `path`
       breaks the digest chain resolution (Check 42 fails with confusing
       "file not found" for an entry that shouldn't exist). Sibling of
       Check 289 (evidence count + uniqueness) / Check 317 (sha256 format)
       for the aio-manifest evidence-entry structural completeness axis.
       (BLOCKING)

  319. `.well-known/aio-manifest.json` every evidence entry `path` MUST
       resolve to an actually existing file at ROOT/<path>. Drift = a
       rename or deletion leaves an entry claiming digest coverage of a
       phantom file. Check 219 verifies `path ⊆ whitelist keys` but the
       whitelist itself could point at deleted files; this Check closes
       that leak by hitting the filesystem directly. Sibling of
       Check 219 (path ⊆ MANIFEST_PATH_TO_LOCAL) / Check 42 (digest
       chain resolves) for the aio-manifest evidence-path existence
       axis. (BLOCKING)

  320. `robots.txt` MUST contain exactly one `Sitemap:` directive line.
       Per RFC 9309 (Robots Exclusion Protocol) multiple Sitemap:
       directives are permitted, but our project contract expects a
       single canonical sitemap.xml. Drift = duplicate `Sitemap:` lines
       yield inconsistent crawler behavior (some crawl all, some pick
       last), or 0 lines silently loses AIO discovery. Sibling of
       Check 35 (Sitemap: directive presence) / Check 279 (Sitemap:
       HTTPS) for the robots.txt Sitemap-directive cardinality axis.
       (BLOCKING)

  386. sitemap.xml every page `<loc>` URL (the `<url><loc>` entries, NOT
       `<image:loc>`) MUST resolve to an existing local file at ROOT.
       Drift = renaming/deleting an advertised resource (llms-full.txt,
       AI2AI.md, .well-known/*, docs/evidence/*, …) without updating
       sitemap.xml, so the sitemap advertises a URL that 404s to AI
       crawlers — a broken AIO discovery surface (the very thing the
       sitemap exists to serve). Check 311 guards `<lastmod>` format and
       Check 312 guards `<loc>` uniqueness, but neither hits the
       filesystem; Check 358 resolves `<image:loc>` only. This closes the
       page-`<loc>` existence leak. Sibling of Check 358 (image:loc
       resolves) / Check 319 (aio-manifest evidence.path resolves) /
       Check 133-135 (file-exists ⟹ wired) for the sitemap page-loc
       existence axis. (BLOCKING)

  446. **実行可能な WebMCP ツール ⟺ discovery 層の宣言 (双方向・BLOCKING)**: shipped JS が
       `navigator.modelContext.registerTool({name: ...})` で登録する**実行可能な**ツールと、
       `.well-known/mcp.json` の `runtime: webmcp` entry が一致すること。
       446a 登録 ⟹ 宣言 (**今日の欠落を捕捉する方向**) / 446b 宣言 ⟹ 登録。
       動機 (2026-08-23 実測): サイトは実行可能な WebMCP ツールを 1 つ登録しているのに、
       **AIO 公開面のどこにも宣言が無かった** —— 記載は開発者向け doc だけ。しかも mcp.json は
       `capabilities.tools = false` と宣言しており、**「ツールは無い」と言いながら 1 つ動いている**
       状態だった (書かれた当時は正確で、ツール追加時に更新されなかった)。
       本セッションで繰り返し掘った「宣言と実態の乖離」の**逆向き** —— 届いているのに宣言が無い。
       ツール名は **main.js から導出**する (決め打ちすると rename 時に Check だけが古い名前を持つ)。
  387. AIO discovery pointer files — `.well-known/api-catalog` (RFC 9727
       linkset) and `.well-known/mcp.json` — every same-origin (canonical
       origin + `/portfolio/`) URL reference (href / service-meta /
       resource URLs) MUST resolve to an existing local file at ROOT.
       These are the entry points AI agents actively DEREFERENCE to
       discover the site's machine-readable resources; a dangling pointer
       (file renamed/deleted without updating the catalog) gives the agent
       a 404 for a declared service — silent breakage of the agent-facing
       AIO discovery layer. Check 165 validates api-catalog structure
       (JSON / linkset / anchor canonical) but NOT href existence; Check
       386 covers sitemap.xml (search-crawler surface) but not these
       (agent surface). Sibling of Check 386 (sitemap page-loc) / Check
       165 (api-catalog structure) / Check 319 (evidence.path) for the
       AIO agent-discovery pointer existence axis. (BLOCKING)

"""
import re
import json
from urllib.parse import unquote


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 311. sitemap.xml <lastmod> strict YYYY-MM-DD AND not future (BLOCKING) ────
    # 全 <lastmod> が strict YYYY-MM-DD 形式かつ today 以下であることを強制。
    # malformed date や future date による crawl priority 操作 drift を封じる。
    _sitemap311 = ROOT / "sitemap.xml"
    if _sitemap311.exists():
        from datetime import date as _date311
        _sm_src311 = _sitemap311.read_text(encoding="utf-8")
        _lastmods311 = re.findall(r"<lastmod>([^<]+)</lastmod>", _sm_src311)
        _strict_re311 = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        _bad_fmt311 = [v for v in _lastmods311 if not _strict_re311.match(v)]
        _today311 = _date311.today()
        _future311: list[str] = []
        for _v in _lastmods311:
            if _strict_re311.match(_v):
                try:
                    if _date311.fromisoformat(_v) > _today311:
                        _future311.append(_v)
                except ValueError:
                    _bad_fmt311.append(_v)
        _ok311 = (not _bad_fmt311) and (not _future311) and len(_lastmods311) > 0
        check(
            _ok311,
            f"Check 311: sitemap.xml <lastmod> {len(_lastmods311)} 件すべて YYYY-MM-DD 形式かつ未来日付なし",
            (f"Check 311: sitemap.xml <lastmod> 違反: bad_format={_bad_fmt311!r} / "
             f"future_dates={_future311!r} — 厳格 crawler に reject される or "
             "crawl priority 不正操作。strict YYYY-MM-DD で今日以前の値へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 311: sitemap.xml present",
              "Check 311: sitemap.xml が無い", blocking=True)

    # ── 312. sitemap.xml <loc> URLs are unique (BLOCKING) ────────────────────────
    # 全 <loc> が重複無しであることを強制。copy-paste drift や
    # lastmod/priority 上書きの silent loss を封じる。
    _sitemap312 = ROOT / "sitemap.xml"
    if _sitemap312.exists():
        _sm_src312 = _sitemap312.read_text(encoding="utf-8")
        _locs312 = re.findall(r"<loc>([^<]+)</loc>", _sm_src312)
        _seen312: set[str] = set()
        _dupes312: list[str] = []
        for _u in _locs312:
            if _u in _seen312 and _u not in _dupes312:
                _dupes312.append(_u)
            _seen312.add(_u)
        _ok312 = (not _dupes312) and len(_locs312) > 0
        check(
            _ok312,
            f"Check 312: sitemap.xml <loc> {len(_locs312)} 件すべて unique",
            (f"Check 312: sitemap.xml <loc> 重複: {_dupes312!r} — "
             "copy-paste drift / lastmod/priority silent overwrite。"
             "重複エントリを削除せよ"),
            blocking=True,
        )
    else:
        check(False, "Check 312: sitemap.xml present",
              "Check 312: sitemap.xml が無い", blocking=True)

    # ── 313. aio-manifest.json generated_at + last_metadata_update NOT future ─────
    # (BLOCKING) — TZ ずれや誤編集による未来 timestamp を封じる。Check 243/273/311
    # の aio-manifest.json 日付軸版。
    _mani313 = ROOT / ".well-known" / "aio-manifest.json"
    if _mani313.exists():
        from datetime import date as _date313
        try:
            _md313 = json.loads(_mani313.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _md313 = None
        if _md313 is not None:
            _today313 = _date313.today()
            _futures313: list[str] = []
            for _field in ("generated_at", "last_metadata_update"):
                _v = _md313.get(_field, "")
                if not _v:
                    continue
                _m = re.match(r"^(\d{4}-\d{2}-\d{2})", _v)
                if not _m:
                    continue
                try:
                    if _date313.fromisoformat(_m.group(1)) > _today313:
                        _futures313.append(f"{_field}={_v!r}")
                except ValueError:
                    pass
            _ok313 = not _futures313
            check(
                _ok313,
                f"Check 313: aio-manifest.json generated_at + last_metadata_update 未来日付なし (today={_today313.isoformat()})",
                (f"Check 313: aio-manifest.json 未来日付 detected: {_futures313!r} — "
                 "AI crawler の recency ranking が corruption。today 以下へ修正"),
                blocking=True,
            )
        else:
            check(False, "Check 313: aio-manifest.json parseable",
                  "Check 313: aio-manifest.json が JSON parse 不能", blocking=True)
    else:
        check(False, "Check 313: aio-manifest.json present",
              "Check 313: aio-manifest.json が無い", blocking=True)

    # ── 314. manifest.webmanifest theme_color == index.html meta theme-color ─────
    # (BLOCKING) — PWA install screen と in-browser address bar の色 drift 封じ。
    _webman314 = ROOT / "manifest.webmanifest"
    _html314_path = ROOT / "index.html"
    if _webman314.exists() and _html314_path.exists():
        try:
            _wm314 = json.loads(_webman314.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _wm314 = None
        if _wm314 is not None:
            _wm_theme314 = str(_wm314.get("theme_color", "")).lower()
            _html314 = _html314_path.read_text(encoding="utf-8")
            _meta_themes314 = [
                m.group(1).lower() for m in re.finditer(
                    r'<meta\s+name="theme-color"[^>]*content="([^"]+)"', _html314)
            ]
            # 逆順 (content が先) の書き方にも対応
            _meta_themes314 += [
                m.group(1).lower() for m in re.finditer(
                    r'<meta\s+content="([^"]+)"[^>]*name="theme-color"', _html314)
            ]
            _ok314 = bool(_wm_theme314) and _wm_theme314 in _meta_themes314
            check(
                _ok314,
                f"Check 314: manifest.webmanifest theme_color={_wm_theme314!r} は index.html meta theme-color {_meta_themes314!r} と cross-surface 一致",
                (f"Check 314: manifest.webmanifest theme_color={_wm_theme314!r} が "
                 f"index.html <meta name=\"theme-color\"> 値集合 {_meta_themes314!r} に含まれない — "
                 "PWA install screen と in-browser address bar の色 drift。"
                 "webmanifest 側 or meta 側どちらかを揃えよ"),
                blocking=True,
            )
        else:
            check(False, "Check 314: manifest.webmanifest parseable",
                  "Check 314: manifest.webmanifest が JSON parse 不能", blocking=True)
    else:
        check(False, "Check 314: manifest.webmanifest + index.html present",
              "Check 314: manifest.webmanifest or index.html が無い", blocking=True)

    # ── 315. webmanifest display enum + background_color 6-digit hex (BLOCKING) ──
    _webman315 = ROOT / "manifest.webmanifest"
    if _webman315.exists():
        try:
            _wm315 = json.loads(_webman315.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _wm315 = None
        if _wm315 is not None:
            _display315 = str(_wm315.get("display", ""))
            _bg315 = str(_wm315.get("background_color", ""))
            _valid_display315 = {"fullscreen", "standalone", "minimal-ui", "browser"}
            _display_ok315 = _display315 in _valid_display315
            _bg_ok315 = bool(re.match(r"^#[0-9a-fA-F]{6}$", _bg315))
            _ok315 = _display_ok315 and _bg_ok315
            check(
                _ok315,
                f"Check 315: webmanifest display={_display315!r} ∈ enum + background_color={_bg315!r} 6-digit hex",
                (f"Check 315: webmanifest 違反: "
                 f"display={_display315!r} (allowed={sorted(_valid_display315)}) / "
                 f"background_color={_bg315!r} (must match ^#[0-9a-fA-F]{{6}}$) — "
                 "PWA install prompt drift or splash-screen OS-default gray fallback"),
                blocking=True,
            )
        else:
            check(False, "Check 315: manifest.webmanifest parseable",
                  "Check 315: manifest.webmanifest が JSON parse 不能", blocking=True)
    else:
        check(False, "Check 315: manifest.webmanifest present",
              "Check 315: manifest.webmanifest が無い", blocking=True)

    # ── 316. webmanifest icons[].purpose enum + sizes format (BLOCKING) ──────────
    _webman316 = ROOT / "manifest.webmanifest"
    if _webman316.exists():
        try:
            _wm316 = json.loads(_webman316.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _wm316 = None
        if _wm316 is not None:
            _icons316 = _wm316.get("icons", [])
            _valid_purpose316 = {"any", "maskable", "monochrome"}
            _bad_purpose316: list[str] = []
            _bad_sizes316: list[str] = []
            _sizes_re316 = re.compile(r"^(any|\d+x\d+(\s+\d+x\d+)*)$")
            for _i, _ic in enumerate(_icons316):
                _purpose = str(_ic.get("purpose", "any"))
                for _tok in _purpose.split():
                    if _tok not in _valid_purpose316:
                        _bad_purpose316.append(f"icons[{_i}].purpose 内 token={_tok!r}")
                _sizes = str(_ic.get("sizes", ""))
                if not _sizes_re316.match(_sizes):
                    _bad_sizes316.append(f"icons[{_i}].sizes={_sizes!r}")
            _ok316 = (not _bad_purpose316) and (not _bad_sizes316) and len(_icons316) > 0
            check(
                _ok316,
                f"Check 316: webmanifest icons {len(_icons316)} 件すべて purpose ∈ enum + sizes 形式適合",
                (f"Check 316: webmanifest icons 違反: "
                 f"purpose_bad={_bad_purpose316!r} (allowed={sorted(_valid_purpose316)}) / "
                 f"sizes_bad={_bad_sizes316!r} (must match 'any' or '<W>x<H>' or space-separated list) — "
                 "adaptive-icon が unusable / UA が icon entry を reject"),
                blocking=True,
            )
        else:
            check(False, "Check 316: manifest.webmanifest parseable",
                  "Check 316: manifest.webmanifest が JSON parse 不能", blocking=True)
    else:
        check(False, "Check 316: manifest.webmanifest present",
              "Check 316: manifest.webmanifest が無い", blocking=True)

    # ── 317. aio-manifest.json all sha256 fields strict 64-hex format (BLOCKING) ─
    _mani317 = ROOT / ".well-known" / "aio-manifest.json"
    if _mani317.exists():
        try:
            _md317 = json.loads(_mani317.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _md317 = None
        if _md317 is not None:
            _sha_re317 = re.compile(r"^[0-9a-f]{64}$")
            _bad_sha317: list[str] = []
            _total_sha317 = 0
            for _key in ("source_of_truth", "supporting_evidence", "observational_evidence"):
                for _i, _entry in enumerate(_md317.get(_key, [])):
                    _v = _entry.get("sha256", "")
                    if not _v:
                        continue
                    _total_sha317 += 1
                    if not _sha_re317.match(_v):
                        _bad_sha317.append(f"{_key}[{_i}].sha256={_v!r}")
            _ok317 = (not _bad_sha317) and _total_sha317 > 0
            check(
                _ok317,
                f"Check 317: aio-manifest.json sha256 field {_total_sha317} 件すべて strict ^[0-9a-f]{{64}}$ 形式",
                (f"Check 317: aio-manifest.json sha256 形式違反: {_bad_sha317!r} — "
                 "truncated / uppercase / space-embedded digest。"
                 "厳密な lowercase 64-hex 形式へ揃えよ"),
                blocking=True,
            )
        else:
            check(False, "Check 317: aio-manifest.json parseable",
                  "Check 317: aio-manifest.json が JSON parse 不能", blocking=True)
    else:
        check(False, "Check 317: aio-manifest.json present",
              "Check 317: aio-manifest.json が無い", blocking=True)

    # ── 318. aio-manifest.json evidence entries required fields (BLOCKING) ───────
    _mani318 = ROOT / ".well-known" / "aio-manifest.json"
    if _mani318.exists():
        try:
            _md318 = json.loads(_mani318.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _md318 = None
        if _md318 is not None:
            _req_fields318 = ("path", "role", "sha256")
            _missing318: list[str] = []
            _total_entries318 = 0
            for _key in ("source_of_truth", "supporting_evidence", "observational_evidence"):
                for _i, _e in enumerate(_md318.get(_key, [])):
                    _total_entries318 += 1
                    for _f in _req_fields318:
                        _v = _e.get(_f, "")
                        if not str(_v).strip():
                            _missing318.append(f"{_key}[{_i}].{_f}=<empty|missing>")
            _ok318 = (not _missing318) and _total_entries318 > 0
            check(
                _ok318,
                f"Check 318: aio-manifest.json evidence entry {_total_entries318} 件すべて {{path, role, sha256}} 完備",
                (f"Check 318: aio-manifest.json evidence entry 必須 field 欠落: {_missing318!r} — "
                 "unlabeled evidence / digest chain 解決不可。全 entry に "
                 "path + role + sha256 を non-empty で揃えよ"),
                blocking=True,
            )
        else:
            check(False, "Check 318: aio-manifest.json parseable",
                  "Check 318: aio-manifest.json が JSON parse 不能", blocking=True)
    else:
        check(False, "Check 318: aio-manifest.json present",
              "Check 318: aio-manifest.json が無い", blocking=True)

    # ── 319. aio-manifest evidence.path resolves to existing file (BLOCKING) ─────
    _mani319 = ROOT / ".well-known" / "aio-manifest.json"
    if _mani319.exists():
        try:
            _md319 = json.loads(_mani319.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _md319 = None
        if _md319 is not None:
            _missing319: list[str] = []
            _total319 = 0
            for _key in ("source_of_truth", "supporting_evidence", "observational_evidence"):
                for _i, _e in enumerate(_md319.get(_key, [])):
                    _p = str(_e.get("path", "")).strip()
                    if not _p:
                        continue
                    _total319 += 1
                    if not (ROOT / _p).is_file():
                        _missing319.append(f"{_key}[{_i}].path={_p!r}")
            _ok319 = (not _missing319) and _total319 > 0
            check(
                _ok319,
                f"Check 319: aio-manifest.json evidence.path {_total319} 件すべて existing file",
                (f"Check 319: aio-manifest.json evidence.path が実 file に解決しない: {_missing319!r} — "
                 "rename/deletion で phantom evidence entry。manifest から entry を消すか "
                 "実 file を配置せよ"),
                blocking=True,
            )
        else:
            check(False, "Check 319: aio-manifest.json parseable",
                  "Check 319: aio-manifest.json が JSON parse 不能", blocking=True)
    else:
        check(False, "Check 319: aio-manifest.json present",
              "Check 319: aio-manifest.json が無い", blocking=True)

    # ── 320. robots.txt Sitemap: directive count == 1 (BLOCKING) ─────────────────
    _robots320 = ROOT / "robots.txt"
    if _robots320.exists():
        _rt_src320 = _robots320.read_text(encoding="utf-8")
        _sitemap_lines320 = re.findall(r"(?m)^Sitemap:\s+\S+", _rt_src320)
        _count320 = len(_sitemap_lines320)
        _ok320 = _count320 == 1
        check(
            _ok320,
            f"Check 320: robots.txt Sitemap: directive count = {_count320} (contract: exactly 1)",
            (f"Check 320: robots.txt Sitemap: directive 件数 {_count320} は契約違反 (要 1 件) — "
             "0=AIO discovery 喪失 / 2+=crawler 挙動不定 (some crawl all, some pick last)"),
            blocking=True,
        )
    else:
        check(False, "Check 320: robots.txt present",
              "Check 320: robots.txt が無い", blocking=True)

    # ── 386. sitemap.xml page <loc> URLs resolve to existing local files (BLOCKING) ─
    # 各 <url><loc> (image sitemap の <image:loc> は除外) を canonical origin+base prefix を
    # 剥がしてローカル path に写像し、実 file として存在することを強制。rename/deletion で
    # sitemap が phantom URL を advertise し AI crawler へ 404 を返す AIO discovery 破綻を防ぐ。
    # Check 311/312 は format/uniqueness のみ・Check 358 は <image:loc> のみで、page <loc> の
    # 存在は無検証だった leak を塞ぐ (Check 319 evidence.path / 133-135 wiring と同型)。
    _sitemap386 = ROOT / "sitemap.xml"
    if _sitemap386.is_file():
        _sm386 = _sitemap386.read_text(encoding="utf-8")
        # <loc>...</loc> のみ抽出 (<image:loc> は別タグゆえ本 regex に非マッチ)
        _locs386 = re.findall(r"<loc>\s*([^<]+?)\s*</loc>", _sm386)
        _missing386: list[str] = []
        _total386 = 0
        for _u in _locs386:
            # canonical origin + GitHub Pages project base (/portfolio/) を剥がす
            _rel = re.sub(r"^https?://[^/]+/portfolio/", "", _u.strip())
            _rel = unquote(_rel)
            _total386 += 1
            # root URL (.../portfolio/) は index.html を指す
            _target = (ROOT / "index.html") if _rel == "" else (ROOT / _rel)
            if not _target.is_file():
                _missing386.append(f"{_u!r} → {_rel or 'index.html'!r}")
        _ok386 = (not _missing386) and _total386 > 0
        check(
            _ok386,
            f"Check 386: sitemap.xml page <loc> {_total386} 件すべて existing local file に解決",
            (f"Check 386: sitemap.xml <loc> が実 file に解決しない: {_missing386!r} — "
             "rename/deletion で phantom URL を advertise し AI crawler へ 404。sitemap から "
             "entry を消すか実 file を配置せよ"),
            blocking=True,
        )
    else:
        check(False, "Check 386: sitemap.xml present",
              "Check 386: sitemap.xml が無い", blocking=True)

    # ── 387. AIO discovery pointer files' same-origin refs resolve to existing files (BLOCKING) ─
    # api-catalog (RFC 9727 linkset) と mcp.json は AI エージェントが実際に dereference して
    # サイトの機械可読リソースを discover する entry point。宣言された同一 origin URL が rename/
    # deletion で dangling すると agent は 404 を受け取り agent-facing AIO discovery が silent に
    # 壊れる。Check 165 は api-catalog の構造 (JSON/linkset/anchor) のみ・Check 386 は sitemap
    # (search crawler 面) のみで、この agent 面 pointer の href 存在は無検証だった。
    # 各 JSON を parse し全 string 値を再帰走査、canonical origin+/portfolio/ の URL を実 file 解決。
    # [FIX 2026-08-23] **同一 origin URL = ファイル、とは限らない。** SPA のハッシュルート
    #   (`https://.../portfolio/#/role-split`) は agent 向けの正当な pointer だが file ではない。
    #   前提が狭いまま file 解決を要求すると、**正しい pointer を「404 する」と誤報告する**
    #   (実際に踏んだ: mcp.json へ WebMCP ツールの canonicalRoute を足した瞬間)。
    #   ただの除外にすると**ルートの正しさが誰にも検証されなくなる**ので、
    #   387b が Check 439 と同じ導出でルート解決を検証する (fragment は fragment として検査する)。
    _ROUTE_FRAGS387: list[str] = []

    def _same_origin_rel387(_u):
        if not isinstance(_u, str):
            return None
        if not re.match(r"^https?://[^/]+/portfolio/", _u):
            return None  # external (schemas.agentskills.io 等) は対象外
        _rel = unquote(re.sub(r"^https?://[^/]+/portfolio/", "", _u.strip()))
        if _rel.startswith("#"):
            _ROUTE_FRAGS387.append(_rel)
            return None  # file ではなく SPA ルート — 387b が検査する
        return _rel

    def _walk387(_obj, _out):
        if isinstance(_obj, str):
            _r = _same_origin_rel387(_obj)
            if _r is not None:
                _out.append(_r)
        elif isinstance(_obj, dict):
            for _v in _obj.values():
                _walk387(_v, _out)
        elif isinstance(_obj, list):
            for _v in _obj:
                _walk387(_v, _out)

    _missing387: list[str] = []
    _total387 = 0
    _absent387: list[str] = []
    for _label387, _path387 in (
        ("api-catalog", ROOT / ".well-known" / "api-catalog"),
        ("mcp.json", ROOT / ".well-known" / "mcp.json"),
    ):
        if not _path387.is_file():
            _absent387.append(_label387)
            continue
        try:
            _data387 = json.loads(_path387.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _absent387.append(f"{_label387}(JSON parse 不能)")
            continue
        _refs387: list[str] = []
        _walk387(_data387, _refs387)
        for _rel387 in sorted(set(_refs387)):
            _total387 += 1
            _tgt387 = (ROOT / "index.html") if _rel387 == "" else (ROOT / _rel387)
            if not _tgt387.is_file():
                _missing387.append(f"{_label387}: {_rel387!r}")
    _ok387 = (not _missing387) and (not _absent387) and _total387 > 0
    check(
        _ok387,
        f"Check 387: AIO discovery pointer (api-catalog + mcp.json) same-origin refs {_total387} 件すべて existing file に解決",
        (f"Check 387: AIO discovery pointer が実 file に解決しない: missing={_missing387!r} / "
         f"absent_or_unparseable={_absent387!r} — rename/deletion で agent が dereference する "
         "api-catalog/mcp.json の pointer が dangling し 404。pointer を消すか実 file を配置せよ"),
        blocking=True,
    )

    # ── 387b. discovery pointer の SPA ルート fragment が実ルートへ解決する (BLOCKING) ─────
    # 387 は「同一 origin URL は実 file へ解決する」を見るが、SPA のハッシュルートは file では
    # ないので対象外にした。**ただ除外するとルートの正しさが誰にも検証されなくなる** ——
    # agent が `#/role-splitt` のような typo を dereference すると NotFound へ落ち、
    # 「ツールはあるがルートが違う」という**淡々と緑になる壊れ方**をする (#96-99 の vacuous-hash class)。
    # ルート集合は Check 439 と同じく **router.js から導出**する (決め打ちすると route 追加時に
    # Check だけが古い一覧を持つ)。
    _router387 = ROOT / "js" / "router.js"
    if _ROUTE_FRAGS387 and _router387.exists():
        _rsrc387 = _router387.read_text(encoding="utf-8")
        _am387 = re.search(r"\[([^\]]*)\]\.includes\(app\)", _rsrc387)
        _apps387 = set(re.findall(r"['\"]([a-z0-9_-]+)['\"]", _am387.group(1) if _am387 else ""))
        _tops387 = set(re.findall(r"case\s+'([a-z0-9-]+)':", _rsrc387))

        def _route_ok387(_frag):
            _raw = _frag.lstrip("#").lstrip("/").split("?")[0]
            if _raw in ("", "not-found"):
                return True
            _parts = [_x for _x in _raw.split("/") if _x]
            if not _parts:
                return True
            if _parts[0] == "apps":
                return len(_parts) == 1 or (len(_parts) == 2 and _parts[1] in _apps387)
            return _parts[0] in _tops387

        _badfrag387 = sorted({_f for _f in _ROUTE_FRAGS387 if not _route_ok387(_f)})
        check(
            not _badfrag387,
            f"Check 387b: discovery pointer の SPA ルート {len(set(_ROUTE_FRAGS387))} 件すべてが実ルートへ解決",
            (f"Check 387b: discovery pointer が存在しないルートを指している: {_badfrag387}。"
             "agent が dereference すると NotFound へ落ち、**「ツールはあるがルートが違う」という"
             "淡々と緑になる壊れ方**をする (#96-99 の vacuous-hash class)。"
             "ルート集合は js/router.js から導出しているので、ルートを増やしたら自動追従する"),
            blocking=True,
        )

    # ── 446. 実行可能な WebMCP ツール ⟺ discovery 層の宣言 (双方向・BLOCKING) ──────────
    # 2026-08-23 実測: サイトは `navigator.modelContext.registerTool` で**実行可能な**ツールを
    # 1 つ登録しているのに、**AIO 公開面のどこにも宣言が無かった**。しかも mcp.json は
    # `capabilities.tools = false` と宣言しており、「ツールは無い」と言いながら 1 つ動いていた。
    # 「宣言はあるが届いていない」の**逆向き** —— 届いているのに宣言が無い。
    # 名前は main.js から導出する (決め打ちすると rename 時に Check だけが古い名前を持つ)。
    _mcp446 = ROOT / ".well-known" / "mcp.json"
    _shipped446 = [ROOT / "main.js"] + sorted((ROOT / "js").glob("*.js"))
    _registered446 = set()
    for _f446 in _shipped446:
        _src446 = _f446.read_text(encoding="utf-8")
        for _m446 in re.finditer(r"registerTool\s*\(\s*\{(.{0,400}?)name\s*:\s*[\"']([\w-]+)[\"']",
                                 _src446, re.S):
            _registered446.add(_m446.group(2))
    if not _mcp446.is_file():
        check(False, "", "Check 446: .well-known/mcp.json が無い", blocking=True)
    else:
        try:
            _mj446 = json.loads(_mcp446.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _mj446 = {}
        _declared446 = {_t.get("name") for _t in _mj446.get("tools", [])
                        if isinstance(_t, dict) and _t.get("runtime") == "webmcp"}
        _caps446 = (_mj446.get("capabilities") or {}).get("tools")

        _bad446 = []
        _undeclared446 = sorted(_registered446 - _declared446)
        if _undeclared446:
            _bad446.append(f"登録済だが mcp.json 未宣言 (agent から発見できない): {_undeclared446}")
        _unregistered446 = sorted(_declared446 - _registered446)
        if _unregistered446:
            _bad446.append(f"mcp.json が runtime:webmcp と宣言するが shipped JS で未登録 "
                           f"(agent が呼べない幽霊ツール): {_unregistered446}")
        # capabilities.tools は「実行可能なツールが在るか」の宣言なので実態と一致させる
        if _registered446 and _caps446 is not True:
            _bad446.append(f"実行可能なツールが {len(_registered446)} 件あるのに "
                           f"capabilities.tools = {_caps446!r} —— 「ツールは無い」と宣言している")
        if not _registered446 and _caps446 is True:
            _bad446.append("capabilities.tools = true だが実行可能なツールが 1 件も登録されていない")

        check(
            not _bad446,
            (f"Check 446: 実行可能な WebMCP ツール {len(_registered446)} 件が mcp.json の "
             f"runtime:webmcp 宣言と双方向で一致 (capabilities.tools={_caps446!r})"),
            (f"Check 446: WebMCP ツールの実態と宣言がずれている: {_bad446}。"
             "**登録されているのに宣言が無いと、静的 discovery しかしない agent は"
             "そのツールの存在を知りようがない**。逆に宣言だけあると幽霊ツールを呼びに来る。"
             "ツール名は main.js から導出しているので、rename すれば mcp.json 側も直す必要がある"),
            blocking=True,
        )
