"""
checks_jsonld_structure.py — index.html の JSON-LD の Schema.org 構造 (244-247)
(extracted from checks_shipped_hygiene.py — 2026-11-15・9b)。

**なぜ切り出したか**: checks_shipped_hygiene.py が 958 行で advisory (950) を越えた。予算は上げず (CLAUDE.md §7 の教訓 (8))、
互いに独立した連続の区間 —— index.html の JSON-LD の構造を見る 4 つ —— をそのまま移した。各区間は index.html を自分で読み、
他の区間の変数に依らない。照合の中身と実行の順 (shipped_hygiene の直後) は変えない。

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT by reference (exec 不使用).

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  244. Every top-level node in JSON-LD `@graph` has `@type`: in index.html
       JSON-LD blocks, every direct top-level element of any `@graph`
       array MUST have a non-empty `@type` field. Drift (anonymous node)
       silently makes AI/SEO consumers ignore the node (no type → cannot
       reason about entity) and breaks Schema.org graph traversal.
       Sibling of Check 217 (top-level @id uniqueness) for the top-level
       @type presence axis. (BLOCKING)

  245. JSON-LD FAQPage `mainEntity[]` Q&A structure validity: every
       FAQPage node's `mainEntity` array MUST contain non-empty Question
       entries, each with `@type == "Question"` + non-empty `name` + an
       `acceptedAnswer` object with `@type == "Answer"` + non-empty
       `text`. Drift would silently break Google FAQ rich-result
       eligibility + AI search FAQ ingestion. Sibling of Check 235
       (Article required fields) for the FAQPage required-structure
       surface. (BLOCKING)

  246. JSON-LD BreadcrumbList `itemListElement` Schema.org structure:
       every BreadcrumbList's `itemListElement` array MUST contain
       ListItem entries, each with `@type == "ListItem"`, an integer
       `position`, a non-empty `name`, and an `item` (URL or @id ref).
       Drift would silently break Google breadcrumb rich-result and AI
       site-structure ingestion. Sibling of Check 245 (FAQPage Q&A) for
       the BreadcrumbList required-structure surface. (BLOCKING)

  247. JSON-LD ImageObject/AudioObject/VideoObject have required fields:
       every node with `@type in {ImageObject, AudioObject, VideoObject}`
       MUST have `name` AND at least one of `contentUrl` / `url`. Drift
       (e.g. silent strip of name) would silently break Google Image/
       Audio rich-result and AI/SEO entity-asset linkage. Sibling of
       Check 245 (FAQPage) / Check 246 (BreadcrumbList) for the
       MediaObject required-structure surface. (BLOCKING)

"""
import json
import re


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 244. JSON-LD @graph 全 top-level node has @type (BLOCKING) ────────────────
    # index.html の各 JSON-LD <script> block の top-level `@graph` 配列の全 element に
    # 非空 `@type` がある (anonymous node 不在) ことを BLOCKING 強制。drift で AI/SEO
    # が無 type node を無視し Schema.org graph traversal 不能。
    _idx244 = ROOT / "index.html"
    if _idx244.exists():
        _isrc244 = _idx244.read_text(encoding="utf-8")
        _blocks244 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc244,
            flags=re.DOTALL,
        )
        _violations244: list[str] = []
        _total244 = 0
        for _bi, _blk in enumerate(_blocks244):
            try:
                _data244 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            _g244 = _data244.get("@graph") if isinstance(_data244, dict) else None
            if not isinstance(_g244, list):
                continue
            for _j, _n in enumerate(_g244):
                _total244 += 1
                if not isinstance(_n, dict) or not isinstance(_n.get("@type"), str) or not _n.get("@type").strip():
                    _violations244.append(f"block{_bi}.@graph[{_j}] missing/empty @type")
        _ok244 = _total244 > 0 and not _violations244
        check(
            _ok244,
            f"Check 244: JSON-LD @graph top-level node {_total244} 件全て @type 保有",
            (f"Check 244: @type 不在 node: {_violations244!r} — AI/SEO 無視されて "
             "Schema.org graph traversal 破壊。各 top-level node に @type を付与せよ"
             if _violations244 else
             "Check 244: @graph top-level node 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 244: index.html present",
              "Check 244: index.html が無い", blocking=True)

    # ── 245. JSON-LD FAQPage mainEntity Q&A structure validity (BLOCKING) ─────────
    # index.html JSON-LD の全 FAQPage node の `mainEntity` 配列が Schema.org Q&A 構造
    # (Question + name + acceptedAnswer(Answer + text)) を満たすことを BLOCKING 強制。
    # drift は SILENT に Google FAQ rich-result 失格 + AI search FAQ ingestion 破壊。
    _idx245 = ROOT / "index.html"
    if _idx245.exists():
        _isrc245 = _idx245.read_text(encoding="utf-8")
        _blocks245 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc245,
            flags=re.DOTALL,
        )
        _violations245: list[str] = []
        _q_count245 = 0
        def _walk245(node: object, path: str) -> None:
            nonlocal _q_count245
            if isinstance(node, dict):
                if node.get("@type") == "FAQPage":
                    _me = node.get("mainEntity")
                    if not isinstance(_me, list) or not _me:
                        _violations245.append(f"{path}: FAQPage.mainEntity 欠落/空")
                    else:
                        for _i, _q in enumerate(_me):
                            _q_count245 += 1
                            if not isinstance(_q, dict):
                                _violations245.append(f"{path}.mainEntity[{_i}] non-dict")
                                continue
                            if _q.get("@type") != "Question":
                                _violations245.append(f"{path}.mainEntity[{_i}] @type != Question")
                            _n = _q.get("name")
                            if not isinstance(_n, str) or not _n.strip():
                                _violations245.append(f"{path}.mainEntity[{_i}] name 欠落/空")
                            _a = _q.get("acceptedAnswer")
                            if not isinstance(_a, dict):
                                _violations245.append(f"{path}.mainEntity[{_i}] acceptedAnswer 欠落")
                            else:
                                if _a.get("@type") != "Answer":
                                    _violations245.append(f"{path}.mainEntity[{_i}].acceptedAnswer @type != Answer")
                                _t = _a.get("text")
                                if not isinstance(_t, str) or not _t.strip():
                                    _violations245.append(f"{path}.mainEntity[{_i}].acceptedAnswer.text 欠落/空")
                for k, v in node.items():
                    if isinstance(v, list):
                        for item in v:
                            _walk245(item, f"{path}.{k}")
                    else:
                        _walk245(v, f"{path}.{k}")
            elif isinstance(node, list):
                for i, item in enumerate(node):
                    _walk245(item, f"{path}[{i}]")
        for _bi, _blk in enumerate(_blocks245):
            try:
                _data245 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            _walk245(_data245, f"block{_bi}")
        _ok245 = _q_count245 > 0 and not _violations245
        check(
            _ok245,
            f"Check 245: FAQPage mainEntity Q&A {_q_count245} 件全て Schema.org 構造正",
            (f"Check 245: 違反: {_violations245!r} — Google FAQ rich-result 失格 + "
             "AI FAQ ingestion 破壊。Question+name+acceptedAnswer(Answer+text) 構造へ揃えよ"
             if _violations245 else
             "Check 245: FAQPage mainEntity Q 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 245: index.html present",
              "Check 245: index.html が無い", blocking=True)

    # ── 246. JSON-LD BreadcrumbList itemListElement Schema.org 構造 (BLOCKING) ────
    # index.html JSON-LD 全 BreadcrumbList の `itemListElement` 配列が ListItem +
    # position(int) + name(非空 str) + item(URL/string) を満たすことを BLOCKING 強制。
    # drift で Google breadcrumb rich-result + AI site-structure ingestion 破壊。
    _idx246 = ROOT / "index.html"
    if _idx246.exists():
        _isrc246 = _idx246.read_text(encoding="utf-8")
        _blocks246 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc246,
            flags=re.DOTALL,
        )
        _violations246: list[str] = []
        _items_count246 = 0
        def _walk246(node: object, path: str) -> None:
            nonlocal _items_count246
            if isinstance(node, dict):
                if node.get("@type") == "BreadcrumbList":
                    _ile = node.get("itemListElement")
                    if not isinstance(_ile, list) or not _ile:
                        _violations246.append(f"{path}: itemListElement 欠落/空")
                    else:
                        for _i, _it in enumerate(_ile):
                            _items_count246 += 1
                            if not isinstance(_it, dict):
                                _violations246.append(f"{path}.itemListElement[{_i}] non-dict")
                                continue
                            if _it.get("@type") != "ListItem":
                                _violations246.append(f"{path}.itemListElement[{_i}] @type != ListItem")
                            if not isinstance(_it.get("position"), int) or isinstance(_it.get("position"), bool):  # bool は int の部分型
                                _violations246.append(f"{path}.itemListElement[{_i}] position not int")
                            _n = _it.get("name")
                            if not isinstance(_n, str) or not _n.strip():
                                _violations246.append(f"{path}.itemListElement[{_i}] name 欠落/空")
                            if not isinstance(_it.get("item"), (str, dict)) or not _it.get("item"):  # [2026-11-08] 空や null も不可
                                _violations246.append(f"{path}.itemListElement[{_i}] item 欠落")
                for k, v in node.items():
                    if isinstance(v, list):
                        for item in v:
                            _walk246(item, f"{path}.{k}")
                    else:
                        _walk246(v, f"{path}.{k}")
            elif isinstance(node, list):
                for i, item in enumerate(node):
                    _walk246(item, f"{path}[{i}]")
        for _bi, _blk in enumerate(_blocks246):
            try:
                _data246 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            _walk246(_data246, f"block{_bi}")
        _ok246 = _items_count246 > 0 and not _violations246
        check(
            _ok246,
            f"Check 246: BreadcrumbList itemListElement {_items_count246} 件全て Schema.org 構造正",
            (f"Check 246: 違反: {_violations246!r} — Google breadcrumb rich-result 失格 "
             "+ AI site-structure ingestion 破壊。ListItem+position+name+item へ揃えよ"
             if _violations246 else
             "Check 246: BreadcrumbList items 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 246: index.html present",
              "Check 246: index.html が無い", blocking=True)

    # ── 247. JSON-LD ImageObject/AudioObject/VideoObject 必須 fields (BLOCKING) ───
    # index.html JSON-LD で `@type in {ImageObject, AudioObject, VideoObject}` の
    # node が `name` AND (`contentUrl` OR `url`) を持つことを BLOCKING 強制。drift で
    # Google Image/Audio rich-result 失格 + AI/SEO entity-asset linkage 破壊。
    _MEDIA_TYPES247 = {"ImageObject", "AudioObject", "VideoObject"}
    _idx247 = ROOT / "index.html"
    if _idx247.exists():
        _isrc247 = _idx247.read_text(encoding="utf-8")
        _blocks247 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc247,
            flags=re.DOTALL,
        )
        _violations247: list[str] = []
        _media_count247 = 0
        def _walk247(node: object, path: str) -> None:
            nonlocal _media_count247
            if isinstance(node, dict):
                _t = node.get("@type")
                if isinstance(_t, str) and _t in _MEDIA_TYPES247:
                    _media_count247 += 1
                    _missing = []
                    if not isinstance(node.get("name"), str) or not node.get("name", "").strip():
                        _missing.append("name")
                    if not any(isinstance(node.get(_u), str) and node.get(_u).strip() for _u in ("contentUrl", "url")):  # 空の URL も不可
                        _missing.append("contentUrl|url")
                    if _missing:
                        _violations247.append(f"{path} {_t}: missing {_missing!r}")
                for k, v in node.items():
                    if isinstance(v, list):
                        for item in v:
                            _walk247(item, f"{path}.{k}")
                    else:
                        _walk247(v, f"{path}.{k}")
            elif isinstance(node, list):
                for i, item in enumerate(node):
                    _walk247(item, f"{path}[{i}]")
        for _bi, _blk in enumerate(_blocks247):
            try:
                _data247 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            _walk247(_data247, f"block{_bi}")
        _ok247 = _media_count247 > 0 and not _violations247
        check(
            _ok247,
            f"Check 247: MediaObject {_media_count247} 件全て name + contentUrl|url 保有",
            (f"Check 247: 違反: {_violations247!r} — Google Image/Audio rich-result 失格 "
             "+ AI/SEO entity-asset linkage 破壊。name + contentUrl|url を揃えよ"
             if _violations247 else
             "Check 247: MediaObject 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 247: index.html present",
              "Check 247: index.html が無い", blocking=True)
