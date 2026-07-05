"""
checks_meta_url.py — index.html meta/asset URL resolution & AIO routing coherence checks (175-180)
(extracted from check_repository_consistency.py — check.py split track).

run(ctx) receives shared check()/ROOT by reference (exec 不使用) so exit code / BLOCKING propagation
are byte-equivalent. annotation+def-aware free-var 分析で外部 `_`-var・global-content 依存ゼロ確認済。
nested-fn の module-level `global _accNNN` は run() 内で `nonlocal` へ機械変換 (意味等価)。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  175. package.json `private: true` + name baseline: package.json must declare `"private": true`
       and `"name": "portfolio-aio"`. Silent removal of `private: true` would allow `npm publish`
       to succeed and leak internal dev config to the public npm registry — a security regression
       with no console error. The `name` value anchors npm tooling identification. (BLOCKING)
  176. index.html static JSON-LD `@id` URLs share canonical URL prefix (own-origin only): every
       `"@id": "URL"` in index.html where URL is on this site's origin
       (yutapr0117-design.github.io) must start with the canonical URL prefix (from
       `<link rel="canonical">`). External-origin @id (e.g. nkgr.co.jp for Organization) are
       exempt. Drift would silently break JSON-LD entity graph linking when canonical URL path
       changes (e.g. project rename); the entity's #person/#webpage/#website anchors would still
       use the old prefix and AI crawlers couldn't follow the graph. (BLOCKING)
  177. llms-full.txt `**Version:**` matches main.js SITE_CONFIG.VERSION: the version marker in
       llms-full.txt's authority header must equal `SITE_CONFIG.VERSION` from main.js. Drift would
       silently desync the AI-authoritative context's stated version from the live site —
       AI/agent ingesting llms-full.txt would think they're seeing a different version than
       what's actually deployed. Extends the version-coherence mesh (Check 1/2/3/19) to the
       llms-full.txt surface. (BLOCKING)
  178. `<meta name="ai:repository">` derives from canonical URL: the GitHub repo URL in
       `<meta name="ai:repository">` must equal `https://github.com/<owner>/<repo>` where
       owner+repo are derived from the canonical URL (hostname's first segment + URL path's
       first segment). Drift would silently point AI crawlers to the wrong GitHub repo when
       canonical URL changes (project rename / fork). (BLOCKING)
  179. `<meta name="ai:version">` matches main.js SITE_CONFIG.VERSION: the version string
       declared to AI crawlers in `<meta name="ai:version">` must equal SITE_CONFIG.VERSION
       in main.js. Drift would silently desync the AI-facing version signal from the
       running app's pipeline version, so AI agents would believe they're crawling a
       different version than what's actually deployed. Extends the version-coherence mesh
       (Check 1/2/3/19/177) to the index.html ai:* meta surface. (BLOCKING)
  180. `<meta name="ai:last-modified">` matches main.js SITE_CONFIG.LAST_UPDATED: the
       last-modified date in `<meta name="ai:last-modified">` must equal SITE_CONFIG
       .LAST_UPDATED in main.js. Drift would silently lie to AI crawlers about freshness,
       confusing recency-weighted retrieval (e.g. AI search ranking by ai:last-modified
       could surface a stale view while the app has actually been updated, or vice
       versa). Sibling Check of 179 for the timestamp axis of the ai:* meta surface.
       (BLOCKING)
"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 175. package.json private: true + name baseline (BLOCKING) ─────────────────
    # package.json が `"private": true` と `"name": "portfolio-aio"` を保持することを
    # BLOCKING 強制する。private: true 削除は `npm publish` を成功させ内部 dev config
    # を public npm registry に流出させる security regression (console error 無し)。
    # name は npm tool 識別の anchor。
    _pkg175 = ROOT / "package.json"
    if _pkg175.exists():
        try:
            _pdata175 = json.loads(_pkg175.read_text(encoding="utf-8"))
            _problems175: list[str] = []
            if _pdata175.get("private") is not True:
                _problems175.append(f"private={_pdata175.get('private')!r} (must be True)")
            if _pdata175.get("name") != "portfolio-aio":
                _problems175.append(f"name={_pdata175.get('name')!r} (must be 'portfolio-aio')")
            check(
                not _problems175,
                "Check 175: package.json private: true + name 'portfolio-aio' OK",
                f"Check 175: package.json baseline drift: {_problems175} — "
                "private 削除で `npm publish` が成功し内部 dev config が public npm registry に "
                "流出する security regression。package.json を修正せよ",
                blocking=True,
            )
        except json.JSONDecodeError as e:
            check(False, f"Check 175: package.json parse",
                  f"Check 175: package.json JSON parse 失敗: {e}", blocking=True)
    else:
        check(False, "Check 175: package.json present",
              "Check 175: package.json が無い", blocking=True)

    # ── 176. index.html JSON-LD @id own-origin canonical prefix (BLOCKING) ─────────
    # index.html 静的 JSON-LD の全 `"@id": "URL"` のうち、URL が本サイト origin
    # (yutapr0117-design.github.io) を含むものは canonical URL prefix で始まることを
    # BLOCKING 強制する。external origin (例: nkgr.co.jp) は exempt。drift は SILENT
    # に JSON-LD entity graph linking を破壊 (canonical path 変更時に #person/#webpage
    # anchor が旧 prefix を引きずり AI crawler が graph を辿れない)。
    _idx176 = ROOT / "index.html"
    if _idx176.exists():
        _isrc176 = _idx176.read_text(encoding="utf-8")
        _canon176_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc176
        )
        _canon176 = _canon176_m.group(1) if _canon176_m else None
        _ids176 = re.findall(r'"@id"\s*:\s*"([^"]+)"', _isrc176)
        _own_origin176 = "yutapr0117-design.github.io"
        _own_ids176 = [u for u in _ids176 if _own_origin176 in u]
        _drift176 = [u for u in _own_ids176 if _canon176 and not u.startswith(_canon176)]
        _ok176 = _canon176 is not None and bool(_own_ids176) and not _drift176
        check(
            _ok176,
            f"Check 176: index.html JSON-LD @id (own-origin {len(_own_ids176)} 件) 全て "
            f"canonical {_canon176!r} prefix",
            (f"Check 176: @id prefix drift: canonical={_canon176!r} / drifted={_drift176[:3]}... "
             f"({len(_drift176)} 件) — JSON-LD entity graph linking が崩壊し AI crawler が "
             "#person/#webpage anchor を辿れない。index.html の @id を canonical prefix に揃えよ"
             if _canon176 and _own_ids176 else
             f"Check 176: canonical もしくは own-origin @id 抽出不可 "
             f"(canonical={_canon176} / own_ids={len(_own_ids176)})"),
            blocking=True,
        )
    else:
        check(False, "Check 176: index.html present",
              "Check 176: index.html が無い — JSON-LD @id coherence を検証できない",
              blocking=True)

    # ── 177. llms-full.txt Version marker == main.js SITE_CONFIG.VERSION (BLOCKING) ─
    # llms-full.txt authority header の `**Version:**` 値が main.js SITE_CONFIG.VERSION
    # と一致することを BLOCKING 強制する。drift は SILENT に AI-authoritative context
    # の version 宣言を live site から desync させる (AI/agent が llms-full.txt を
    # 読み込んでも deploy 中の version と違う番号を信じる)。Check 1/2/3/19 の
    # version-coherence mesh を llms-full.txt に拡張。
    _lf177 = ROOT / "llms-full.txt"
    _main177 = ROOT / "main.js"
    if _lf177.exists() and _main177.exists():
        _lsrc177 = _lf177.read_text(encoding="utf-8")
        _msrc177 = _main177.read_text(encoding="utf-8")
        _lver177_m = re.search(r"\*\*Version:\*\*\s*(v[0-9]+)", _lsrc177)
        _sver177_m = re.search(r"VERSION:\s*['\"](v[0-9]+)['\"]", _msrc177)
        _lver177 = _lver177_m.group(1) if _lver177_m else None
        _sver177 = _sver177_m.group(1) if _sver177_m else None
        _ok177 = _lver177 is not None and _sver177 is not None and _lver177 == _sver177
        check(
            _ok177,
            f"Check 177: llms-full.txt Version={_lver177!r} == main.js SITE_CONFIG.VERSION={_sver177!r}",
            (f"Check 177: version drift: llms-full.txt={_lver177!r} / SITE_CONFIG={_sver177!r} — "
             "AI/agent が llms-full.txt を読み込んでも deploy 中の version と違う番号を信じる "
             "(AI-authoritative context の version 宣言が live site から desync)。"
             "llms-full.txt の **Version:** または main.js SITE_CONFIG.VERSION を同期せよ"
             if _lver177 and _sver177 else
             f"Check 177: version 抽出不可 (llms-full={_lver177} / SITE_CONFIG={_sver177})"),
            blocking=True,
        )
    else:
        check(False, "Check 177: llms-full.txt + main.js present",
              "Check 177: llms-full.txt もしくは main.js が無い", blocking=True)

    # ── 178. <meta name=ai:repository> derives from canonical URL (BLOCKING) ───────
    # `<meta name="ai:repository">` の content URL が canonical URL から派生する
    # GitHub repo URL (`https://github.com/<owner>/<repo>`) と一致することを BLOCKING
    # 強制する。owner+repo は canonical URL の hostname 第 1 segment (例
    # yutapr0117-design.github.io → yutapr0117-design) と URL path 第 1 segment
    # (例 /portfolio/ → portfolio) から導出。drift は SILENT に AI crawler を別 repo
    # へ誘導する。
    _idx178 = ROOT / "index.html"
    if _idx178.exists():
        _isrc178 = _idx178.read_text(encoding="utf-8")
        _canon178_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc178
        )
        _repo178_m = re.search(
            r'<meta\s+name=["\']ai:repository["\']\s+content=["\']([^"\']+)["\']', _isrc178
        )
        _canon178 = _canon178_m.group(1) if _canon178_m else None
        _ai_repo178 = _repo178_m.group(1) if _repo178_m else None
        _expected178 = None
        if _canon178:
            from urllib.parse import urlparse as _urlparse178
            _parsed178 = _urlparse178(_canon178)
            # hostname e.g. yutapr0117-design.github.io → owner = yutapr0117-design
            _host_parts178 = (_parsed178.hostname or "").split(".")
            _owner178 = _host_parts178[0] if _host_parts178 else ""
            # path e.g. /portfolio/ → repo = portfolio
            _path_parts178 = [p for p in (_parsed178.path or "").split("/") if p]
            _repo_name178 = _path_parts178[0] if _path_parts178 else ""
            if _owner178 and _repo_name178:
                _expected178 = f"https://github.com/{_owner178}/{_repo_name178}"
        _ok178 = (
            _canon178 is not None
            and _ai_repo178 is not None
            and _expected178 is not None
            and _ai_repo178 == _expected178
        )
        check(
            _ok178,
            f"Check 178: ai:repository={_ai_repo178!r} は canonical URL 由来 ({_expected178!r})",
            (f"Check 178: ai:repository drift: ai:repository={_ai_repo178!r} / "
             f"expected={_expected178!r} (canonical={_canon178!r} から導出) — "
             "AI crawler が別 GitHub repo へ誘導される。index.html ai:repository を "
             "canonical URL 由来 GitHub URL に揃えよ"
             if _canon178 and _ai_repo178 else
             f"Check 178: canonical / ai:repository 抽出不可 "
             f"(canonical={_canon178} / ai:repository={_ai_repo178})"),
            blocking=True,
        )
    else:
        check(False, "Check 178: index.html present",
              "Check 178: index.html が無い", blocking=True)

    # ── 179. <meta name=ai:version> matches main.js SITE_CONFIG.VERSION (BLOCKING) ─
    # index.html の `<meta name="ai:version">` content と main.js SITE_CONFIG.VERSION が
    # byte-identical であることを BLOCKING 強制。drift は SILENT に AI-facing version
    # signal を deploy 中の version から desync (AI agent は ai:version を読んで pipeline
    # version を判断するため、誤値 = 旧 release の挙動を期待して crawl)。Check 177 が
    # llms-full.txt 軸を被覆するのに対し本 Check は ai:* meta 軸を被覆。
    _idx179 = ROOT / "index.html"
    _main179 = ROOT / "main.js"
    if _idx179.exists() and _main179.exists():
        _isrc179 = _idx179.read_text(encoding="utf-8")
        _msrc179 = _main179.read_text(encoding="utf-8")
        _ai_ver179_m = re.search(
            r'<meta\s+name=["\']ai:version["\']\s+content=["\']([^"\']+)["\']', _isrc179
        )
        _site_ver179_m = re.search(
            r"VERSION:\s*['\"]([^'\"]+)['\"]", _msrc179
        )
        _ai_ver179 = _ai_ver179_m.group(1) if _ai_ver179_m else None
        _site_ver179 = _site_ver179_m.group(1) if _site_ver179_m else None
        _ok179 = (
            _ai_ver179 is not None
            and _site_ver179 is not None
            and _ai_ver179 == _site_ver179
        )
        check(
            _ok179,
            f"Check 179: ai:version={_ai_ver179!r} == main.js SITE_CONFIG.VERSION={_site_ver179!r}",
            (f"Check 179: ai:version drift: ai:version={_ai_ver179!r} / "
             f"SITE_CONFIG.VERSION={_site_ver179!r} — AI crawler に旧 version を信じさせる。"
             "index.html ai:version を SITE_CONFIG.VERSION と揃えよ"
             if _ai_ver179 and _site_ver179 else
             f"Check 179: ai:version / SITE_CONFIG.VERSION 抽出不可 "
             f"(ai:version={_ai_ver179} / SITE_CONFIG.VERSION={_site_ver179})"),
            blocking=True,
        )
    else:
        check(False, "Check 179: index.html + main.js present",
              "Check 179: index.html または main.js が無い", blocking=True)

    # ── 180. <meta name=ai:last-modified> matches main.js SITE_CONFIG.LAST_UPDATED (BLOCKING) ─
    # index.html の `<meta name="ai:last-modified">` content と main.js
    # SITE_CONFIG.LAST_UPDATED が byte-identical であることを BLOCKING 強制。drift は
    # SILENT に AI crawler の freshness signal を破壊し、recency-weighted retrieval に
    # stale-view または不当に新しい view を見せうる。Check 179 (ai:version) の timestamp 軸版。
    _idx180 = ROOT / "index.html"
    _main180 = ROOT / "main.js"
    if _idx180.exists() and _main180.exists():
        _isrc180 = _idx180.read_text(encoding="utf-8")
        _msrc180 = _main180.read_text(encoding="utf-8")
        _ai_lm180_m = re.search(
            r'<meta\s+name=["\']ai:last-modified["\']\s+content=["\']([^"\']+)["\']', _isrc180
        )
        _site_lm180_m = re.search(
            r"LAST_UPDATED:\s*['\"]([^'\"]+)['\"]", _msrc180
        )
        _ai_lm180 = _ai_lm180_m.group(1) if _ai_lm180_m else None
        _site_lm180 = _site_lm180_m.group(1) if _site_lm180_m else None
        _ok180 = (
            _ai_lm180 is not None
            and _site_lm180 is not None
            and _ai_lm180 == _site_lm180
        )
        check(
            _ok180,
            f"Check 180: ai:last-modified={_ai_lm180!r} == main.js SITE_CONFIG.LAST_UPDATED={_site_lm180!r}",
            (f"Check 180: ai:last-modified drift: ai:last-modified={_ai_lm180!r} / "
             f"SITE_CONFIG.LAST_UPDATED={_site_lm180!r} — AI crawler の freshness 信号が "
             "deploy 実時刻から desync。index.html ai:last-modified を SITE_CONFIG.LAST_UPDATED と揃えよ"
             if _ai_lm180 and _site_lm180 else
             f"Check 180: ai:last-modified / SITE_CONFIG.LAST_UPDATED 抽出不可 "
             f"(ai:last-modified={_ai_lm180} / SITE_CONFIG.LAST_UPDATED={_site_lm180})"),
            blocking=True,
        )
    else:
        check(False, "Check 180: index.html + main.js present",
              "Check 180: index.html または main.js が無い", blocking=True)
