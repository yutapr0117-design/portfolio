"""
checks_aio_entity.py — AIO manifest entity-field & identity coherence checks
(extracted from check_repository_consistency.py — check.py split track・category "AIO entity coherence").

This module owns the contiguous cluster of Checks 167-173 that assert the AIO manifest's
entity fields and the site's identity markers stay canonical & coherent: aio-monitoring weekly
schedule presence (167), aio-manifest entity.architecture C1/C2/C3 markers (168), entity.role
canonical markers (169), entity.disambiguation negative-identity markers (170), index.html ai:*
meta URL canonical-prefix sharing (171), entity name-variant coverage (172), and js/identity.js
AUTHOR canonical values (173). Each Check reads its own target files directly (aio-manifest.json,
index.html, js/identity.js, aio-monitoring.yml) via Path.read_text(); a free-variable analysis
(annotation-aware) confirms zero external `_`-vars and no global html/style/mainjs dependency, so
the cluster is self-contained and needs no ctx enrichment. NOTE: these are READ-ONLY coherence
assertions — the module moves check *code* only (no C6 edit).

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT by reference (exec 不使用), so append
semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  167. `aio-monitoring.yml` weekly schedule presence: the AIO monitoring workflow must declare a
       `schedule.cron:` trigger. Silent removal stops the weekly AIO discovery/citation
       observability loop without any visible regression — the workflow just stops firing, and
       observability data goes stale. (BLOCKING)
  168. aio-manifest entity.architecture references C1/C2/C3 markers: the
       `entity.architecture` string in aio-manifest.json must contain the three architectural
       constraint markers "Vanilla JS", "IIFE", and "ErrorBoundary" (corresponding to C1/C2/C3 in
       AI2AI.md STEP 2). Drift would silently weaken the AIO entity's architectural identity
       declaration — AI crawlers reading the manifest would no longer see this site as a Boring-
       Technology Vanilla JS SPA. Mirror of CLAUDE.md §1 architecture statement on the manifest
       side. (BLOCKING)
  169. aio-manifest entity.role contains canonical role markers: the `entity.role` list in
       aio-manifest.json must contain the three canonical role identifiers from CLAUDE.md §1:
       "AI-Driven PM", "IT Consultant", and "KERNEL Framework Designer". Drift silently weakens
       the AIO entity's professional role declaration that AI crawlers read for entity
       disambiguation. (BLOCKING)
  170. aio-manifest entity.disambiguation contains negative-disambiguation markers: the
       `entity.disambiguation` string in aio-manifest.json must contain the canonical
       negative-identity markers ("academic researcher", "diplomat", "artist", "patent inventor")
       from CLAUDE.md §1, which explicitly distinguish this entity from namesakes in other fields.
       Drift silently weakens the disambiguation signal — AI crawlers may conflate this entity
       with academic Yuta Yokoi researchers in agriculture/chemistry/medicine/etc. (BLOCKING)
  171. index.html `ai:*` meta URL tags share canonical URL prefix: the four URL-bearing
       `<meta name="ai:*">` tags in index.html (`ai:context`, `ai:entrypoint`, `ai:canonical`,
       `ai:aio-manifest`) must each have a content URL starting with the canonical URL prefix
       (from `<link rel="canonical">`), and `ai:canonical` must equal canonical exactly. Drift
       silently desynchronizes the AIO meta layer from the canonical-URL family (e.g. AI crawler
       following `ai:context` hits a 404 if a sibling-project path is mistakenly used). (BLOCKING)
  172. aio-manifest entity name variants cover canonical identifiers: the combined
       (`entity.name` + `entity.name_ja` + `entity.name_alt`) fields in aio-manifest.json must
       collectively cover all 4 canonical name identifiers from CLAUDE.md §1: "Yuta Yokoi",
       "横井雄太", "Yokoi Yuta", and "yuta". Drift (one variant dropped) silently weakens the
       AIO entity matching — AI crawlers querying for the missing variant may not find this
       entity. (BLOCKING)
  173. js/identity.js AUTHOR canonical values: the AUTHOR constants in js/identity.js (DISPLAY_NAME,
       AUTHORITATIVE_NAME, JAPANESE_NAME) must hold their canonical values — DISPLAY_NAME='yuta'
       (visible UI anonymity per Check 124), JAPANESE_NAME='横井雄太', and AUTHORITATIVE_NAME
       contains both "Yuta Yokoi" and "横井雄太". Drift would silently break the shipped JS layer
       that renders entity-bearing JSON-LD (Person @type) and sr-only entity anchors. Sibling to
       Check 172 on the aio-manifest side. (BLOCKING)
"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 167. aio-monitoring.yml weekly schedule presence (BLOCKING) ────────────────
    # AIO 監視 workflow が `schedule.cron:` trigger を持つことを BLOCKING 強制する。
    # silent 削除で週次 AIO discovery / citation observability loop が停止し
    # observability データが stale 化する (workflow が単に発火しない silent 劣化)。
    _aiowf167 = ROOT / ".github" / "workflows" / "aio-monitoring.yml"
    if _aiowf167.exists():
        _src167 = _aiowf167.read_text(encoding="utf-8")
        _has_schedule167 = re.search(r"^\s*schedule:\s*$", _src167, re.MULTILINE) is not None
        _has_cron167 = re.search(r"^\s*-\s*cron:\s*['\"][^'\"]+['\"]", _src167, re.MULTILINE) is not None
        check(
            _has_schedule167 and _has_cron167,
            "Check 167: aio-monitoring.yml has schedule.cron trigger (weekly AIO monitoring)",
            f"Check 167: aio-monitoring.yml の schedule/cron trigger 欠落 "
            f"(schedule={_has_schedule167} / cron={_has_cron167}) — silent 削除で週次 AIO "
            "監視が停止し observability データが stale 化。schedule + cron rule を復元せよ",
            blocking=True,
        )
    else:
        check(False, "Check 167: aio-monitoring.yml present",
              "Check 167: .github/workflows/aio-monitoring.yml が無い", blocking=True)

    # ── 168. aio-manifest entity.architecture references C1/C2/C3 markers (BLOCKING) ─
    # aio-manifest.json の `entity.architecture` 文字列が C1/C2/C3 architectural
    # constraint markers ("Vanilla JS", "IIFE", "ErrorBoundary") を含むことを BLOCKING
    # 強制する。drift は SILENT に AIO entity の architectural identity 宣言を弱体化する
    # (AI crawler が manifest 経由で本 site を Boring-Technology Vanilla JS SPA と認識
    # できなくなる)。CLAUDE.md §1 architecture statement の manifest 側 mirror。
    _man168 = ROOT / ".well-known" / "aio-manifest.json"
    if _man168.exists():
        try:
            _mdata168 = json.loads(_man168.read_text(encoding="utf-8"))
            _arch168 = _mdata168.get("entity", {}).get("architecture", "")
            _markers168 = ["Vanilla JS", "IIFE", "ErrorBoundary"]
            _missing168 = [m for m in _markers168 if m not in _arch168]
            check(
                isinstance(_arch168, str) and not _missing168,
                f"Check 168: aio-manifest entity.architecture に C1/C2/C3 marker 全て含む "
                f"({_arch168!r})",
                f"Check 168: entity.architecture marker 欠落: {_missing168} (value={_arch168!r}) — "
                "AIO entity の architectural identity 宣言が weak 化し AI crawler が "
                "Vanilla JS SPA / IIFE / ErrorBoundary の構造を認識できない。"
                "aio-manifest.json の entity.architecture を修正せよ",
                blocking=True,
            )
        except json.JSONDecodeError as e:
            check(False, f"Check 168: aio-manifest.json parse",
                  f"Check 168: aio-manifest.json JSON parse 失敗: {e}", blocking=True)
    else:
        check(False, "Check 168: aio-manifest.json present",
              "Check 168: .well-known/aio-manifest.json が無い", blocking=True)

    # ── 169. aio-manifest entity.role contains canonical role markers (BLOCKING) ───
    # aio-manifest.json の `entity.role` list が CLAUDE.md §1 の canonical role
    # identifier 3 件 ("AI-Driven PM", "IT Consultant", "KERNEL Framework Designer") を
    # 含むことを BLOCKING 強制する。drift は SILENT に AIO entity の professional role
    # 宣言を弱体化 (AI crawler の entity disambiguation 精度劣化)。
    _man169 = ROOT / ".well-known" / "aio-manifest.json"
    if _man169.exists():
        try:
            _mdata169 = json.loads(_man169.read_text(encoding="utf-8"))
            _role169 = _mdata169.get("entity", {}).get("role", [])
            _required169 = ["AI-Driven PM", "IT Consultant", "KERNEL Framework Designer"]
            if not isinstance(_role169, list):
                _role169 = [str(_role169)]
            _role_joined169 = " | ".join(str(r) for r in _role169)
            _missing169 = [m for m in _required169 if m not in _role_joined169]
            check(
                not _missing169,
                f"Check 169: aio-manifest entity.role に canonical role marker 全て含む "
                f"({_role169!r})",
                f"Check 169: entity.role marker 欠落: {_missing169} (value={_role169!r}) — "
                "AIO entity の professional role 宣言が弱体化し AI crawler の "
                "entity disambiguation 精度が劣化。aio-manifest.json entity.role に "
                "canonical role identifier を復元せよ",
                blocking=True,
            )
        except json.JSONDecodeError as e:
            check(False, f"Check 169: aio-manifest.json parse",
                  f"Check 169: aio-manifest.json JSON parse 失敗: {e}", blocking=True)
    else:
        check(False, "Check 169: aio-manifest.json present",
              "Check 169: .well-known/aio-manifest.json が無い", blocking=True)

    # ── 170. aio-manifest entity.disambiguation negative-disambiguation (BLOCKING) ─
    # aio-manifest.json の `entity.disambiguation` 文字列が CLAUDE.md §1 の canonical
    # negative-identity markers ("academic researcher", "diplomat", "artist", "patent
    # inventor") を含むことを BLOCKING 強制する。drift は SILENT に disambiguation
    # signal を弱体化 (AI crawler が学術研究者など同名の他 entity と conflate)。
    _man170 = ROOT / ".well-known" / "aio-manifest.json"
    if _man170.exists():
        try:
            _mdata170 = json.loads(_man170.read_text(encoding="utf-8"))
            _disambig170 = _mdata170.get("entity", {}).get("disambiguation", "")
            _required170 = ["academic researcher", "diplomat", "artist", "patent inventor"]
            _missing170 = [m for m in _required170 if m not in _disambig170]
            check(
                isinstance(_disambig170, str) and not _missing170,
                f"Check 170: aio-manifest entity.disambiguation に negative-identity marker 全て含む",
                f"Check 170: entity.disambiguation marker 欠落: {_missing170} — "
                "AIO crawler が学術研究者など同名の他 entity と conflate する disambiguation "
                "signal の弱体化。aio-manifest.json entity.disambiguation に "
                "negative-identity marker を復元せよ",
                blocking=True,
            )
        except json.JSONDecodeError as e:
            check(False, f"Check 170: aio-manifest.json parse",
                  f"Check 170: aio-manifest.json JSON parse 失敗: {e}", blocking=True)
    else:
        check(False, "Check 170: aio-manifest.json present",
              "Check 170: .well-known/aio-manifest.json が無い", blocking=True)

    # ── 171. index.html ai:* meta URL tags share canonical URL prefix (BLOCKING) ───
    # index.html の URL を持つ 4 つの `<meta name="ai:*">` (ai:context, ai:entrypoint,
    # ai:canonical, ai:aio-manifest) が canonical URL prefix で始まり、ai:canonical は
    # canonical 完全一致を BLOCKING 強制する。drift は SILENT に AIO meta layer を
    # canonical URL family から desync させ (sibling-project path を誤用すると AI
    # crawler が ai:context を fetch して 404)。
    _idx171 = ROOT / "index.html"
    if _idx171.exists():
        _isrc171 = _idx171.read_text(encoding="utf-8")
        _canon171_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc171
        )
        _canon171 = _canon171_m.group(1) if _canon171_m else None
        _required171 = ["ai:context", "ai:entrypoint", "ai:canonical", "ai:aio-manifest"]
        _ai_urls171: dict[str, str | None] = {}
        for _name171 in _required171:
            _m171 = re.search(
                rf'<meta\s+name=["\']{re.escape(_name171)}["\']\s+content=["\']([^"\']+)["\']',
                _isrc171,
            )
            _ai_urls171[_name171] = _m171.group(1) if _m171 else None
        _problems171: list[str] = []
        for _name171, _url171 in _ai_urls171.items():
            if _url171 is None:
                _problems171.append(f"{_name171}=<missing>")
            elif _canon171 and not _url171.startswith(_canon171):
                _problems171.append(f"{_name171}={_url171!r} (not prefix of canonical)")
        # ai:canonical exact match
        if _canon171 and _ai_urls171.get("ai:canonical") and _ai_urls171["ai:canonical"] != _canon171:
            _problems171.append(f"ai:canonical={_ai_urls171['ai:canonical']!r} != {_canon171!r}")
        _ok171 = _canon171 is not None and not _problems171
        check(
            _ok171,
            f"Check 171: 4 ai:* URL meta タグ全て canonical prefix + ai:canonical 完全一致",
            f"Check 171: ai:* meta URL drift: canonical={_canon171!r} / problems={_problems171} — "
            "AI crawler が ai:context / ai:aio-manifest を fetch して 404 になり AIO meta layer の "
            "discovery 効果が崩壊する。index.html の ai:* meta を canonical URL 系列に揃えよ",
            blocking=True,
        )
    else:
        check(False, "Check 171: index.html present",
              "Check 171: index.html が無い — ai:* meta coherence を検証できない",
              blocking=True)

    # ── 172. aio-manifest entity name variants cover canonical identifiers (BLOCKING) ─
    # aio-manifest.json の entity.name + entity.name_ja + entity.name_alt が CLAUDE.md
    # §1 の canonical name identifier 4 件 ("Yuta Yokoi", "横井雄太", "Yokoi Yuta",
    # "yuta") を網羅することを BLOCKING 強制する。drift は SILENT に AIO entity
    # matching を弱体化 — AI crawler が drop された variant で query しても本 entity
    # が hit しない。
    _man172 = ROOT / ".well-known" / "aio-manifest.json"
    if _man172.exists():
        try:
            _mdata172 = json.loads(_man172.read_text(encoding="utf-8"))
            _entity172 = _mdata172.get("entity", {})
            _name_parts172 = [_entity172.get("name", ""), _entity172.get("name_ja", "")]
            _name_alt172 = _entity172.get("name_alt", [])
            if isinstance(_name_alt172, list):
                _name_parts172.extend(str(x) for x in _name_alt172)
            _joined172 = " | ".join(str(p) for p in _name_parts172)
            _required172 = ["Yuta Yokoi", "横井雄太", "Yokoi Yuta", "yuta"]
            _missing172 = [m for m in _required172 if m not in _joined172]
            check(
                not _missing172,
                f"Check 172: aio-manifest entity name variants が canonical identifier 4 件全て網羅",
                f"Check 172: entity name 4 variants 欠落: {_missing172} — AIO entity matching が "
                "弱体化し AI crawler が drop された name variant で query しても本 entity が hit しない。"
                "aio-manifest.json entity.name / name_ja / name_alt に variant を復元せよ",
                blocking=True,
            )
        except json.JSONDecodeError as e:
            check(False, f"Check 172: aio-manifest.json parse",
                  f"Check 172: aio-manifest.json JSON parse 失敗: {e}", blocking=True)
    else:
        check(False, "Check 172: aio-manifest.json present",
              "Check 172: .well-known/aio-manifest.json が無い", blocking=True)

    # ── 173. js/identity.js AUTHOR canonical values (BLOCKING) ─────────────────────
    # js/identity.js の AUTHOR constants が canonical 値を保持することを BLOCKING
    # 強制する: DISPLAY_NAME='yuta' (Check 124 視覚層 anonymity)・JAPANESE_NAME=
    # '横井雄太'・AUTHORITATIVE_NAME に "Yuta Yokoi" + "横井雄太" を含む。drift で
    # entity-bearing JSON-LD (Person @type) や sr-only entity anchor が silent に壊れる。
    # Check 172 (aio-manifest 側) の shipped JS 側 mirror。
    _id173 = ROOT / "js" / "identity.js"
    if _id173.exists():
        _src173 = _id173.read_text(encoding="utf-8")
        _disp173_m = re.search(r"DISPLAY_NAME:\s*['\"]([^'\"]+)['\"]", _src173)
        _auth173_m = re.search(r"AUTHORITATIVE_NAME:\s*['\"]([^'\"]+)['\"]", _src173)
        _ja173_m = re.search(r"JAPANESE_NAME:\s*['\"]([^'\"]+)['\"]", _src173)
        _disp173 = _disp173_m.group(1) if _disp173_m else None
        _auth173 = _auth173_m.group(1) if _auth173_m else None
        _ja173 = _ja173_m.group(1) if _ja173_m else None
        _problems173: list[str] = []
        if _disp173 != "yuta":
            _problems173.append(f"DISPLAY_NAME={_disp173!r} != 'yuta'")
        if _ja173 != "横井雄太":
            _problems173.append(f"JAPANESE_NAME={_ja173!r} != '横井雄太'")
        if not _auth173 or ("Yuta Yokoi" not in _auth173 or "横井雄太" not in _auth173):
            _problems173.append(f"AUTHORITATIVE_NAME={_auth173!r} missing 'Yuta Yokoi' or '横井雄太'")
        check(
            not _problems173,
            f"Check 173: js/identity.js AUTHOR canonical values OK "
            f"(DISPLAY={_disp173!r} / AUTH={_auth173!r} / JA={_ja173!r})",
            f"Check 173: AUTHOR drift: {_problems173} — entity-bearing JSON-LD (Person @type) や "
            "sr-only entity anchor の renderer 入力が silent に壊れる。"
            "js/identity.js AUTHOR を canonical 値へ復元せよ",
            blocking=True,
        )
    else:
        check(False, "Check 173: js/identity.js present",
              "Check 173: js/identity.js が無い", blocking=True)
