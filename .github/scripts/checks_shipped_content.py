"""
checks_shipped_content.py — shipped-JS content-scan + JSON-LD length checks (236/238/266/267/268)
(extracted from check_repository_consistency.py — check.py split track).

run(ctx) receives shared check()/ROOT/read/extract by reference (exec 不使用) so exit code / BLOCKING
propagation are byte-equivalent. 各 Check は対象 file を自前 read。annotation+def-aware free-var 確認済。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  236. aio-manifest.json `generated_at` is strict RFC 3339 datetime AND
       affiliation `start_date` is strict YYYY-MM-DD: the `generated_at`
       top-level field must match `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$`
       and `entity.affiliation.start_date` must match `^\d{4}-\d{2}-\d{2}$`
       AND parse as a real calendar date/time. Sibling of Check 93
       (last_metadata_update format) for the generated_at + start_date
       fields. Drift would silently corrupt recency / employment-timeline
       signals consumed by AI/SEO. (BLOCKING)

  238. HTML head singleton tags each appear exactly once: index.html must
       contain exactly 1 of each of `<title>`, `<link rel="canonical">`,
       `<meta name="description">`, `<meta property="og:url">`,
       `<meta property="og:title">`. Multiple instances are SILENT class
       drift — browsers/crawlers pick "first" or "last" non-deterministically
       and the duplicate dilutes the canonical entity signal. Sibling of
       Check 17/180 (date sync) for the head singleton uniqueness axis.
       (BLOCKING)

  266. JSON-LD entity description length in [20, 1000]: every Person /
       Organization / ImageObject / CreativeWork node with a `description`
       field must have its description in [20, 1000] character length.
       Below 20: too brief to be useful for AI/SEO. Above 1000: usually
       indicates copy-paste of full body text into description (Google
       Schema.org spec recommends concise summary). Sibling of Check 224
       (meta description length) for the JSON-LD entity description axis.
       (BLOCKING)

  267. JSON-LD entity name length in [3, 200]: every Person / Organization
       / ImageObject / WebSite / WebPage / TechArticle / CreativeWork /
       AudioObject node with `@id` AND `name` field must have name length
       in [3, 200] character. Drift: <3 = stub/empty (entity disambiguation
       impossible); >200 = copy-paste over-long (often body text leaked).
       Sibling of Check 266 (entity description length) for the JSON-LD
       entity name axis. (BLOCKING)

  268. JSON-LD Article / TechArticle headline length in [10, 110]:
       every Article/TechArticle node with `headline` field MUST have
       length in [10, 110] character. Schema.org / Google Article
       rich-result spec recommends headline <= 110 char (else card
       truncates). <10 = sparse / no value for SERP card. Sibling of
       Check 235 (Article required fields) for the headline length axis.
       (BLOCKING)

"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    read = ctx.read
    extract = ctx.extract

    # ── 236. aio-manifest.json generated_at + start_date strict format (BLOCKING) ─
    # aio-manifest.json `generated_at` が RFC 3339 (YYYY-MM-DDTHH:MM:SSZ) で
    # `entity.affiliation.start_date` が YYYY-MM-DD で実在 datetime/date であることを
    # BLOCKING 強制。Check 93 (last_metadata_update format) の generated_at +
    # start_date 軸補完。drift は SILENT に recency / 雇用 timeline 信号を corruption。
    from datetime import date as _date236, datetime as _dt236
    _man236 = ROOT / ".well-known" / "aio-manifest.json"
    if _man236.exists():
        try:
            _md236 = json.loads(_man236.read_text(encoding="utf-8"))
        except json.JSONDecodeError as _e236:
            _md236 = None
        _bad236: list[str] = []
        if isinstance(_md236, dict):
            _gen236 = _md236.get("generated_at")
            if not isinstance(_gen236, str):
                _bad236.append(f"generated_at 欠落 / 非 string ({_gen236!r})")
            elif not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", _gen236):
                _bad236.append(f"generated_at={_gen236!r} (format)")
            else:
                try:
                    _dt236.strptime(_gen236, "%Y-%m-%dT%H:%M:%SZ")
                except ValueError as _e:
                    _bad236.append(f"generated_at={_gen236!r} ({_e})")
            _sd236 = (
                _md236.get("entity", {}).get("affiliation", {}).get("start_date")
                if isinstance(_md236.get("entity"), dict) else None
            )
            if not isinstance(_sd236, str):
                _bad236.append(f"affiliation.start_date 欠落 / 非 string ({_sd236!r})")
            elif not re.match(r"^\d{4}-\d{2}-\d{2}$", _sd236):
                _bad236.append(f"affiliation.start_date={_sd236!r} (format)")
            else:
                try:
                    _y, _mo, _d = _sd236.split("-")
                    _date236(int(_y), int(_mo), int(_d))
                except (ValueError, TypeError) as _e:
                    _bad236.append(f"affiliation.start_date={_sd236!r} ({_e})")
        else:
            _bad236.append("aio-manifest parse 失敗")
        _ok236 = not _bad236
        check(
            _ok236,
            f"Check 236: aio-manifest generated_at + affiliation.start_date 共に strict ISO format",
            (f"Check 236: 違反: {_bad236!r} — recency/雇用 timeline 信号 corruption。"
             "strict ISO format へ揃えよ"),
            blocking=True,
        )
    else:
        check(False, "Check 236: aio-manifest.json present",
              "Check 236: aio-manifest.json が無い", blocking=True)

    # ── 238. HTML head singleton tags appear exactly once (BLOCKING) ──────────────
    # index.html の head 内 singleton tag (title / link rel=canonical /
    # meta name=description / meta property=og:url / meta property=og:title) が
    # それぞれちょうど 1 件で存在することを BLOCKING 強制。複数 instance は SILENT
    # に browser/crawler が「first」「last」を非決定的に選び canonical signal を希釈。
    _idx238 = ROOT / "index.html"
    if _idx238.exists():
        _isrc238 = _idx238.read_text(encoding="utf-8")
        _patterns238 = [
            ("<title>", r"<title>[^<]+</title>"),
            ('<link rel="canonical">', r'<link\s+rel=["\']canonical["\']'),
            ('<meta name="description">', r'<meta\s+name=["\']description["\']'),
            ('<meta property="og:url">', r'<meta\s+property=["\']og:url["\']'),
            ('<meta property="og:title">', r'<meta\s+property=["\']og:title["\']'),
        ]
        _bad238: list[str] = []
        for _label, _pat in _patterns238:
            _n = len(re.findall(_pat, _isrc238))
            if _n != 1:
                _bad238.append(f"{_label} count={_n} (expected 1)")
        _ok238 = not _bad238
        check(
            _ok238,
            f"Check 238: HTML head singleton tags 全て exactly 1 件",
            (f"Check 238: singleton 違反: {_bad238!r} — browser/crawler が非決定的に "
             "選択し canonical signal が希釈。各 head singleton tag を exactly 1 件へ整理"),
            blocking=True,
        )
    else:
        check(False, "Check 238: index.html present",
              "Check 238: index.html が無い", blocking=True)

    # ── 266. JSON-LD entity description length in [20, 1000] (BLOCKING) ───────────
    # index.html JSON-LD で Person/Organization/ImageObject/CreativeWork node の
    # description 値長が [20, 1000] character 内であることを BLOCKING 強制。
    # 下限以下: too brief / 上限以上: copy-paste over-long。Check 224 の JSON-LD 軸版。
    _DESC_TYPES266 = {"Person", "Organization", "ImageObject", "CreativeWork"}
    _idx266 = ROOT / "index.html"
    if _idx266.exists():
        _isrc266 = _idx266.read_text(encoding="utf-8")
        _blocks266 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc266,
            flags=re.DOTALL,
        )
        _violations266: list[str] = []
        _checked266 = 0
        def _walk266(node: object, path: str) -> None:
            nonlocal _checked266
            if isinstance(node, dict):
                _t = node.get("@type")
                _d = node.get("description")
                if isinstance(_t, str) and _t in _DESC_TYPES266 and isinstance(_d, str):
                    _checked266 += 1
                    _ln = len(_d)
                    if not (20 <= _ln <= 1000):
                        _violations266.append(f"{path} {_t}: description len={_ln} (band [20, 1000] 違反)")
                for k, v in node.items():
                    if isinstance(v, list):
                        for item in v:
                            _walk266(item, f"{path}.{k}")
                    else:
                        _walk266(v, f"{path}.{k}")
            elif isinstance(node, list):
                for i, item in enumerate(node):
                    _walk266(item, f"{path}[{i}]")
        for _bi, _blk in enumerate(_blocks266):
            try:
                _walk266(json.loads(_blk), f"block{_bi}")
            except json.JSONDecodeError:
                continue
        _ok266 = _checked266 > 0 and not _violations266
        check(
            _ok266,
            f"Check 266: JSON-LD entity description ({_checked266} 件) 全て [20, 1000] 内",
            (f"Check 266: 違反: {_violations266!r} — too brief で AI/SEO 入力不足 / "
             "too long で copy-paste 過剰。20〜1000 char へ調整せよ"
             if _violations266 else
             "Check 266: description 付き entity 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 266: index.html present",
              "Check 266: index.html が無い", blocking=True)

    # ── 267. JSON-LD entity name length in [3, 200] (BLOCKING) ────────────────────
    # index.html JSON-LD で @id + name 両備の entity (Person/Organization/Image/
    # WebSite/WebPage/TechArticle/CreativeWork/AudioObject) の name 値長が
    # [3, 200] 内であることを BLOCKING 強制。Check 266 の entity name 軸版。
    _NAME_TYPES267 = {"Person", "Organization", "ImageObject", "WebSite", "WebPage",
                       "TechArticle", "CreativeWork", "AudioObject"}
    _idx267 = ROOT / "index.html"
    if _idx267.exists():
        _isrc267 = _idx267.read_text(encoding="utf-8")
        _blocks267 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc267,
            flags=re.DOTALL,
        )
        _violations267: list[str] = []
        _checked267 = 0
        def _walk267(node: object, path: str) -> None:
            nonlocal _checked267
            if isinstance(node, dict):
                _t = node.get("@type")
                _n = node.get("name")
                if (
                    isinstance(_t, str) and _t in _NAME_TYPES267
                    and node.get("@id") and isinstance(_n, str)
                ):
                    _checked267 += 1
                    _ln = len(_n)
                    if not (3 <= _ln <= 200):
                        _violations267.append(f"{path} {_t}: name len={_ln} value={_n[:30]!r}")
                for k, v in node.items():
                    if isinstance(v, list):
                        for item in v:
                            _walk267(item, f"{path}.{k}")
                    else:
                        _walk267(v, f"{path}.{k}")
            elif isinstance(node, list):
                for i, item in enumerate(node):
                    _walk267(item, f"{path}[{i}]")
        for _bi, _blk in enumerate(_blocks267):
            try:
                _walk267(json.loads(_blk), f"block{_bi}")
            except json.JSONDecodeError:
                continue
        _ok267 = _checked267 > 0 and not _violations267
        check(
            _ok267,
            f"Check 267: JSON-LD entity name ({_checked267} 件) 全て [3, 200] 内",
            (f"Check 267: 違反: {_violations267!r} — <3=stub / >200=copy-paste over-long。"
             "[3, 200] へ調整"
             if _violations267 else
             "Check 267: name 付き entity 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 267: index.html present",
              "Check 267: index.html が無い", blocking=True)

    # ── 268. JSON-LD Article/TechArticle headline length in [10, 110] (BLOCKING) ──
    # index.html JSON-LD Article/TechArticle node の headline 値長が [10, 110] 内
    # (Schema.org / Google Article rich-result spec) であることを BLOCKING 強制。
    # Check 235 (Article 必須 fields) の headline length 軸版。
    _HEADLINE_TYPES268 = {"Article", "TechArticle", "NewsArticle", "BlogPosting"}
    _idx268 = ROOT / "index.html"
    if _idx268.exists():
        _isrc268 = _idx268.read_text(encoding="utf-8")
        _blocks268 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc268,
            flags=re.DOTALL,
        )
        _violations268: list[str] = []
        _checked268 = 0
        def _walk268(node: object, path: str) -> None:
            nonlocal _checked268
            if isinstance(node, dict):
                _t = node.get("@type")
                _h = node.get("headline")
                if isinstance(_t, str) and _t in _HEADLINE_TYPES268 and isinstance(_h, str):
                    _checked268 += 1
                    _ln = len(_h)
                    if not (10 <= _ln <= 110):
                        _violations268.append(f"{path} {_t}: headline len={_ln}")
                for k, v in node.items():
                    if isinstance(v, list):
                        for item in v:
                            _walk268(item, f"{path}.{k}")
                    else:
                        _walk268(v, f"{path}.{k}")
            elif isinstance(node, list):
                for i, item in enumerate(node):
                    _walk268(item, f"{path}[{i}]")
        for _bi, _blk in enumerate(_blocks268):
            try:
                _walk268(json.loads(_blk), f"block{_bi}")
            except json.JSONDecodeError:
                continue
        _ok268 = _checked268 > 0 and not _violations268
        check(
            _ok268,
            f"Check 268: Article/TechArticle headline ({_checked268} 件) 全て [10, 110] 内",
            (f"Check 268: 違反: {_violations268!r} — Google rich-result card truncate "
             "or sparse。Schema.org spec の <= 110 char に揃えよ"
             if _violations268 else
             "Check 268: headline 付き Article 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 268: index.html present",
              "Check 268: index.html が無い", blocking=True)
