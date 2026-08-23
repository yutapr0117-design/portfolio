"""
checks_api_catalog.py — `.well-known/api-catalog` (RFC 9727) discovery surface の Check 群
(extracted from checks_seo_meta.py — check.py split track・category "api catalog").

`/.well-known/api-catalog` は「このサイトの API / AIO 入口は何か」に対する機械可読な真値で、
RFC 9727 (IETF) + RFC 9264 (linkset) + RFC 6573 (`item` 関係) の 3 仕様に同時に従う必要がある。
この面の drift は **視覚に一切出ず**、behavior e2e にも screenshot にも現れないため、仕様適合
だけが唯一の検証手段になる。実際に「メンバー 7 件すべてを `api-catalog` 関係で列挙する」誤り
(= 全メンバーを『別のカタログ』と偽って宣言する) が長期間残存していた。

各 Check は `.well-known/api-catalog` と `index.html` を直接読む。monolith の共有 global には
依存しないため ctx enrichment は不要。

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/warnings by reference (exec 不使用) so append
semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  165. `.well-known/api-catalog` JSON + anchor canonical origin: `.well-known/api-catalog` must be
       valid JSON with a `linkset` array containing at least one entry, and the `anchor` URL of the
       first linkset entry must start with the canonical URL (from `<link rel="canonical">`). A
       drift / malformed file silently breaks AI crawler discovery of authoritative API endpoints
       (the catalog is the entry point that points to mcp.json / agent-skills / aio-manifest /
       llms-full). (BLOCKING)

  449. `.well-known/api-catalog` RFC 9727 relation semantics: RFC 9727 §2 lists a catalog's members
       under the `item` relation (RFC 6573); the `api-catalog` relation *inside* a catalog means
       **nesting** — a link to another API catalog. Listing plain resources under `api-catalog`
       therefore declares "these are all catalogs", and a spec-conformant agent will try to parse
       `llms-full.txt` as a linkset and fail. All 7 entries were in that state until 2026-08-23;
       Check 165 only validates JSON shape and the anchor origin, so no layer saw the relation
       error. 449a bounds `api-catalog` to actual catalog URLs (genuine nesting stays legal),
       449b keeps `service-desc`/`service-meta`/`service-doc`/`status` out of link objects (they
       are *relation types* per RFC 9264, expressed as separate anchored contexts, not target
       attributes), 449c requires a string `href` on every link object. (BLOCKING)
"""
import json
import re


def run(ctx):
    """Execute this module's checks against the shared context.

    ctx exposes: ROOT (Path), check (callable), warnings (list), errors (list),
    read/read_bytes/extract (helpers). Extracted checks use the same objects the
    monolith uses, so appends land in the same errors/warnings lists.
    """
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 165. .well-known/api-catalog JSON + anchor canonical origin (BLOCKING) ─────
    # `.well-known/api-catalog` が valid JSON + linkset array (≥1 entry) + 最初 entry の
    # anchor URL が canonical URL prefix を持つことを BLOCKING 強制する。drift は
    # SILENT に AI crawler の API endpoint discovery を破壊する (catalog は mcp.json /
    # agent-skills / aio-manifest / llms-full への entry-point pointer)。
    _ac165 = ROOT / ".well-known" / "api-catalog"
    _idx165 = ROOT / "index.html"
    if _ac165.exists() and _idx165.exists():
        _isrc165 = _idx165.read_text(encoding="utf-8")
        _canon165_m = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', _isrc165
        )
        _canon165 = _canon165_m.group(1) if _canon165_m else None
        _ok165 = False
        _err165 = ""
        try:
            _ac_data165 = json.loads(_ac165.read_text(encoding="utf-8"))
            _linkset165 = _ac_data165.get("linkset")
            if not isinstance(_linkset165, list) or not _linkset165:
                _err165 = f"linkset が array/非空 でない (type={type(_linkset165).__name__})"
            else:
                _anchor165 = _linkset165[0].get("anchor")
                if not isinstance(_anchor165, str):
                    _err165 = f"linkset[0].anchor が文字列でない ({_anchor165!r})"
                elif not _canon165:
                    _err165 = "canonical URL を index.html から抽出できない"
                elif not _anchor165.startswith(_canon165):
                    _err165 = f"anchor={_anchor165!r} が canonical {_canon165!r} で始まらない"
                else:
                    _ok165 = True
        except json.JSONDecodeError as e:
            _err165 = f"JSON parse 失敗: {e}"
        check(
            _ok165,
            f"Check 165: .well-known/api-catalog valid JSON + anchor starts with canonical "
            f"({_canon165!r})",
            f"Check 165: .well-known/api-catalog 整合 fail: {_err165} — AI crawler の API "
            "endpoint discovery が silent に崩壊する。.well-known/api-catalog を修正せよ",
            blocking=True,
        )
    else:
        check(False, "Check 165: .well-known/api-catalog + index.html present",
              "Check 165: .well-known/api-catalog もしくは index.html が無い",
              blocking=True)

    # ── 449. api-catalog RFC 9727 relation semantics (BLOCKING) ───────────────────
    # RFC 9727 §2 はカタログ**内部**での列挙関係を `item` (RFC 6573) と定めており、
    # `api-catalog` 関係は「**別の API カタログへの入れ子**」を意味する。メンバーを
    # `api-catalog` で並べると「これらは全てカタログだ」と偽って宣言することになり、
    # 仕様に従う agent はメンバーを linkset として parse しようとして失敗する。
    # 2026-08-23 に 7 件すべてがこの状態だった (Check 165 は JSON 構造と anchor しか
    # 見ないため、関係型の誤りを検出する層が存在しなかった)。
    # 449a: カタログ context の `api-catalog` 配下はカタログ URL に限る (入れ子は許可)
    # 449b: service-desc / service-meta / service-doc / status は**関係型**であって
    #       target attribute ではない (RFC 9264) — link object 内に混ぜない
    # 449c: 全 link object が文字列 href を持つ
    _ac449 = ROOT / ".well-known" / "api-catalog"
    if _ac449.exists():
        _REL449 = ("service-desc", "service-meta", "service-doc", "status")
        _bad_nest449, _bad_attr449, _bad_href449 = [], [], []
        try:
            _ls449 = json.loads(_ac449.read_text(encoding="utf-8")).get("linkset") or []
        except json.JSONDecodeError:
            _ls449 = []          # Check 165 が JSON 妥当性を BLOCKING で担当
        for _ctx449 in _ls449:
            if not isinstance(_ctx449, dict):
                continue
            for _rel449, _links449 in _ctx449.items():
                if _rel449 == "anchor" or not isinstance(_links449, list):
                    continue
                for _ln449 in _links449:
                    if not isinstance(_ln449, dict):
                        continue
                    _h449 = _ln449.get("href")
                    if not isinstance(_h449, str) or not _h449:
                        _bad_href449.append(f"{_rel449}: href={_h449!r}")
                        continue
                    if _rel449 == "api-catalog" and not _h449.rstrip("/").endswith(
                        "/.well-known/api-catalog"
                    ):
                        _bad_nest449.append(_h449)
                    for _k449 in _REL449:
                        if _k449 in _ln449:
                            _bad_attr449.append(f"{_h449} に {_k449}")
        check(
            not _bad_nest449,
            "Check 449a: api-catalog 関係は入れ子カタログのみを指す (RFC 9727)",
            "Check 449a: `api-catalog` 関係がカタログでない URL を指している: "
            + "; ".join(_bad_nest449)
            + " — RFC 9727 でこの関係は『別の API カタログへの入れ子』を意味する。"
            "カタログのメンバーは `item` (RFC 6573) で列挙せよ",
            blocking=True,
        )
        check(
            not _bad_attr449,
            "Check 449b: service-* / status を link object の attribute に混ぜない",
            "Check 449b: 関係型を target attribute として使っている: "
            + "; ".join(_bad_attr449)
            + " — RFC 9264 でこれらは**関係型**。対象リソースを `anchor` とする別 "
            "context として表現せよ",
            blocking=True,
        )
        check(
            not _bad_href449,
            "Check 449c: api-catalog の全 link object が文字列 href を持つ",
            "Check 449c: href が無い/文字列でない link object: " + "; ".join(_bad_href449),
            blocking=True,
        )
    else:
        check(False, "Check 449: .well-known/api-catalog present",
              "Check 449: .well-known/api-catalog が無い — RFC 9727 関係型を検証できない",
              blocking=True)

