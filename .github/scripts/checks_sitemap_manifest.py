"""
checks_sitemap_manifest.py — sitemap & manifest format/validity coherence checks (311-320)
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

"""
import re
import json


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
