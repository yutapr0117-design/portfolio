"""
checks_asset_resolve.py — shipped-asset resolution wiring checks — preload href / sitemap image:loc + og:image / BGM audio (357-359)
(extracted from check_repository_consistency.py — check.py split track).

run(ctx) receives shared check()/ROOT by reference (exec 不使用) so exit code / BLOCKING propagation
are byte-equivalent. annotation+def-aware free-var 分析で外部 `_`-var・global-content 依存ゼロ確認済。
nested-fn の module-level `global _accNNN` は run() 内で `nonlocal` へ機械変換 (意味等価)。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  357. Every LOCAL `<link rel="preload">` href in index.html (relative
       `./x` or canonical `/portfolio/x`, i.e. not a cross-origin
       `https://` URL) MUST resolve to an existing file in the working
       tree. Check 53 covers `rel="modulepreload"`; this covers plain
       `rel="preload"` (currently the hero WebP LCP preload). Drift =
       renaming the hero asset while updating og:image / sitemap but
       missing the preload href leaves a 404 preload — wasted bandwidth
       AND the hero LCP element is not actually preloaded (LCP
       regression), silently (screenshot advisory). Sibling of Check 53
       (modulepreload resolution) / Check 326 (preload as= value) for the
       preload href-resolution axis. (BLOCKING)

  358. sitemap.xml image-sitemap coherence: every `<image:loc>` URL MUST
       (a) resolve (after stripping the canonical prefix) to an existing
       local file, AND (b) the `<meta property="og:image">` content URL
       MUST appear among the `<image:loc>` set (hero cross-surface
       agreement). Drift = renaming the hero asset and updating og:image
       but missing the sitemap `<image:loc>` (or vice versa) points Google
       Images at a 404 / a different image than the social card. Sibling
       of Check 164 (og:image resolves) / Check 297 (canonical entry has
       image:image) for the image-sitemap resolution+coherence axis.
       (BLOCKING)

  359. BGM audio wiring: index.html MUST contain an `<audio id="bgm-audio">`
       element (the id that the `BGM` manager in js/ui-components.js reads
       via `getElementById('bgm-audio')`), AND its `src` MUST resolve to
       an existing local file. Drift = removing/renaming the id silently
       no-ops the BGM toggle (`_audio()` returns null); a stale src
       (renaming the mp3 while updating JSON-LD/sitemap/asset:audio:canonical
       but missing the `<audio src>`) makes playback 404 with only a
       `console.warn('BGM play failed')` that no behavior e2e observes.
       Sibling of Check 357 (preload resolution) / Check 335 (manifest
       link wiring) for the BGM audio element-wiring axis. (BLOCKING)

"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 357. local <link rel="preload"> href resolves to a file (BLOCKING) ───────
    # Check 53 は modulepreload を被覆。本 Check は plain preload (hero WebP LCP) の
    # local href が実 file に解決することを強制。href drift で 404 preload = LCP miss。
    _idx357 = ROOT / "index.html"
    if _idx357.is_file():
        _h357 = _idx357.read_text(encoding="utf-8")
        _h357_nc = re.sub(r"<!--.*?-->", "", _h357, flags=re.DOTALL)
        _preload_tags357 = re.findall(r'<link\s+[^>]*rel="preload"[^>]*>', _h357_nc)
        _missing357: list[str] = []
        _checked357 = 0
        for _tag in _preload_tags357:
            _mh = re.search(r'href="([^"]+)"', _tag)
            if not _mh:
                continue
            _href = _mh.group(1)
            # cross-origin (https://) は working tree で解決不可ゆえ scope 外
            if _href.startswith("http://") or _href.startswith("https://"):
                continue
            _checked357 += 1
            _rel = _href
            for _pfx in ("/portfolio/", "./", "/"):
                if _rel.startswith(_pfx):
                    _rel = _rel[len(_pfx):]
                    break
            if not (ROOT / _rel).is_file():
                _missing357.append(f"{_href} (→ {_rel})")
        _ok357 = (not _missing357) and _checked357 > 0
        check(
            _ok357,
            f"Check 357: local preload href {_checked357} 件すべて実 file に解決",
            (f"Check 357: local preload href が file 解決しない: {_missing357!r} — "
             "hero asset rename 等で preload href が取り残されると 404 preload = 帯域浪費 + "
             "hero LCP element が preload されず LCP 回帰 (silent)。href を実 file へ揃えよ"
             if _checked357 > 0 else
             "Check 357: local (非 cross-origin) preload href が 0 件 (hero WebP preload の期待値)"),
            blocking=True,
        )
    else:
        check(False, "Check 357: index.html present",
              "Check 357: index.html が無い", blocking=True)

    # ── 358. sitemap <image:loc> resolution + og:image coherence (BLOCKING) ──────
    _sitemap358 = ROOT / "sitemap.xml"
    _idx358 = ROOT / "index.html"
    if _sitemap358.is_file() and _idx358.is_file():
        _sm358 = _sitemap358.read_text(encoding="utf-8")
        _image_locs358 = re.findall(r"<image:loc>([^<]+)</image:loc>", _sm358)
        _problems358: list[str] = []
        # (a) 各 image:loc が実 file に解決
        for _url in _image_locs358:
            _rel = _url.strip()
            for _pfx in ("https://yutapr0117-design.github.io/portfolio/",
                         "/portfolio/", "./", "/"):
                if _rel.startswith(_pfx):
                    _rel = _rel[len(_pfx):]
                    break
            if not (ROOT / _rel).is_file():
                _problems358.append(f"image:loc {_url.strip()!r} が file 解決しない")
        # (b) og:image が image:loc 集合に含まれる (hero cross-surface 一致)
        _h358 = re.sub(r"<!--.*?-->", "", _idx358.read_text(encoding="utf-8"), flags=re.DOTALL)
        _og358 = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', _h358)
        if _og358:
            _og_url358 = _og358.group(1)
            if _og_url358 not in [u.strip() for u in _image_locs358]:
                _problems358.append(
                    f"og:image {_og_url358!r} が image:loc 集合 {[u.strip() for u in _image_locs358]!r} に不在")
        _ok358 = (not _problems358) and len(_image_locs358) > 0
        check(
            _ok358,
            f"Check 358: sitemap image:loc {len(_image_locs358)} 件が実 file 解決 + og:image と cross-surface 一致",
            (f"Check 358: image-sitemap coherence drift: {_problems358!r} — "
             "hero rename で og:image / image:loc の片方が取り残されると Google Images が "
             "404 / social card と別画像を指す。両者を hero canonical URL へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 358: sitemap.xml + index.html present",
              "Check 358: sitemap.xml または index.html が無い", blocking=True)

    # ── 359. BGM <audio id="bgm-audio"> element wiring + src resolution (BLOCKING) ─
    # BGM manager (js/ui-components.js) は getElementById('bgm-audio') に依存。
    # element 不在で toggle が silent no-op、src drift で playback 404。
    _idx359 = ROOT / "index.html"
    if _idx359.is_file():
        _h359 = _idx359.read_text(encoding="utf-8")
        _h359_nc = re.sub(r"<!--.*?-->", "", _h359, flags=re.DOTALL)
        _problems359: list[str] = []
        # (a) <audio ... id="bgm-audio" ...> が存在する
        _audio_m359 = re.search(r'<audio\b[^>]*\bid="bgm-audio"[^>]*>', _h359_nc, re.DOTALL)
        if not _audio_m359:
            # 属性順序が id が先のケースにも対応
            _audio_m359 = re.search(r'<audio\b(?=[^>]*\bid="bgm-audio")[^>]*>', _h359_nc, re.DOTALL)
        if not _audio_m359:
            _problems359.append('<audio id="bgm-audio"> element が不在 (BGM manager の getElementById が null)')
        else:
            # (b) src が実 file に解決
            _src_m359 = re.search(r'src="([^"]+)"', _audio_m359.group(0))
            if not _src_m359:
                _problems359.append('<audio id="bgm-audio"> に src 属性が無い')
            else:
                _src359 = _src_m359.group(1)
                _rel359 = _src359
                for _pfx in ("https://yutapr0117-design.github.io/portfolio/",
                             "/portfolio/", "./", "/"):
                    if _rel359.startswith(_pfx):
                        _rel359 = _rel359[len(_pfx):]
                        break
                if not (ROOT / _rel359).is_file():
                    _problems359.append(f'bgm-audio src {_src359!r} が file 解決しない (→ {_rel359})')
        _ok359 = not _problems359
        check(
            _ok359,
            "Check 359: <audio id=\"bgm-audio\"> 存在 + src が実 mp3 file に解決 (BGM 配線)",
            (f"Check 359: BGM audio wiring drift: {_problems359!r} — "
             "id 除去で BGM toggle が silent no-op、src drift で playback 404 "
             "(console.warn のみ・behavior e2e 非検査)。element と src を復元せよ"),
            blocking=True,
        )
    else:
        check(False, "Check 359: index.html present",
              "Check 359: index.html が無い", blocking=True)
