"""
checks_jsonld_refs.py — JSON-LD referential integrity checks — @id refs resolve / @id unique / datePublished<=dateModified / manifest paths (216-219)
(extracted from check_repository_consistency.py — check.py split track).

run(ctx) receives shared check()/ROOT by reference (exec 不使用) so exit code / BLOCKING propagation
are byte-equivalent. annotation+def-aware free-var 分析で外部 `_`-var・global-content 依存ゼロ確認済。
nested-fn の module-level `global _accNNN` は run() 内で `nonlocal` へ機械変換 (意味等価)。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  216. JSON-LD `@id` cross-references resolve to defined nodes in the same
       graph (referential integrity): in index.html static JSON-LD blocks,
       any `{"@id": "..."}` reference appearing as the value of common
       reference properties (`author`, `about`, `isPartOf`, `mainEntity`,
       `creator`, `reviewedBy`, `publisher`, `primaryImageOfPage`) must
       point to an `@id` that is defined by some other node in the same
       JSON-LD graph (a node having BOTH `@type` and `@id`). Drift would
       silently fragment the entity graph: AI knowledge-graph consumers
       follow `@id` references and find dead anchors, breaking the linked
       structure of Person/WebSite/WebPage/Organization claims. Check 200
       /201 enforce that primary @ids derive from canonical URL; Check 216
       enforces that every reference actually resolves. (BLOCKING)

  217. JSON-LD `@id` definitions are unique within each `@graph` (BLOCKING):
       in index.html static JSON-LD, no two top-level nodes of the same
       `@graph` array (per `<script type="application/ld+json">` block) may
       claim the same `@id` (with `@type` + `@id`). Drift (e.g. two
       Article nodes both claiming `#article-1`, or accidentally reusing
       `#hero-image` for two assets in the same block) would silently make
       AI / knowledge-graph consumers ambiguous about which node is
       canonical — references via Check 216 would resolve to any one of
       the duplicates non-deterministically. Context-redundant Person
       re-definition across separate JSON-LD blocks (a self-contained
       Article that re-states its creator) is allowed and intentional.
       Sibling of Check 141 (default-project slug/id uniqueness) for the
       JSON-LD entity graph. (BLOCKING)

  218. JSON-LD `datePublished` <= `dateModified` per node (BLOCKING):
       in index.html static JSON-LD, every node containing BOTH
       `datePublished` and `dateModified` must satisfy
       `datePublished <= dateModified` (semantic invariant from Schema.org).
       Drift (e.g. modifying datePublished forward without updating
       dateModified) would silently make AI / SEO crawlers believe the page
       was modified BEFORE it was published — corrupting recency / freshness
       signals and undermining trust. Sibling of Check 208 (ISO-8601 format)
       for the JSON-LD date semantic ordering surface. (BLOCKING)

  497. **index.html の静的な JSON-LD が、読む側の Check の前提の形だけで書かれていること** (BLOCKING・2026-11-08):
       JSON-LD を読む Check は 20 を超え、どれも `<script type="application/ld+json">` の完全一致で塊を探し、
       `@type` を文字列、値を素の文字列として読み、同じ `@id` の最初のノードしか見ない。監査で、引用符の
       無い type 属性・配列の `@type`・型付きの値 (`{"@value": …}`)・矛盾する 2 つ目のノードが、それぞれ
       10 件を超える Check を素通りすると実測した。読む側を 1 つずつ直すより、別の形が在りえないことを
       ここで保証する (Check 238 が meta についてしたのと同じ)。同じ `@id` の 2 つ目以降のノードは、値が
       いちばん大きいノードの値に含まれていれば許す (JSON-LD のノードの統合で意味が変わらない)。
  219. aio-manifest.json declared paths ⊆ check_aio_digests.py
       MANIFEST_PATH_TO_LOCAL keys: every `path` value in aio-manifest.json
       `source_of_truth` / `supporting_evidence` / `observational_evidence`
       MUST appear as a key in `MANIFEST_PATH_TO_LOCAL` dict of
       `.github/scripts/check_aio_digests.py`. Drift (e.g. aio-guardian adds
       a new evidence entry to the manifest but forgets to register it in
       check_aio_digests.py's local-path map) would silently skip digest
       verification for the new path — the manifest could declare any
       sha256, and the tool would never check the actual file against it.
       This invariant catches silent digest-chain gaps that bypass C6.
       (BLOCKING)

"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 216. JSON-LD @id cross-references resolve (referential integrity) (BLOCKING) ─
    # index.html 静的 JSON-LD 内の参照系 property (author/about/isPartOf/mainEntity/
    # creator/reviewedBy/publisher/primaryImageOfPage) の `{"@id": "..."}` 参照が、
    # 同じ graph 内のどこかで `@type` + `@id` を持つ node により定義されていることを
    # BLOCKING 強制。drift は SILENT に entity graph を断片化 — AI/知識グラフ consumer
    # が dead anchor を踏み Person/WebSite/WebPage/Organization 主張の linkage が壊れる。
    _REF_PROPS216 = {
        "author", "about", "isPartOf", "mainEntity", "creator",
        "reviewedBy", "publisher", "primaryImageOfPage",
    }
    _idx216 = ROOT / "index.html"
    if _idx216.exists():
        _isrc216 = _idx216.read_text(encoding="utf-8")
        _blocks216 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc216,
            flags=re.DOTALL,
        )
        _defined_ids216: set[str] = set()
        _ref_ids216: list[tuple[str, str]] = []
        def _walk216(node: object, parent_key: str | None = None) -> None:
            if isinstance(node, dict):
                _is_def = "@type" in node and "@id" in node and isinstance(node.get("@id"), str)
                if _is_def:
                    _defined_ids216.add(node["@id"])
                # reference: object containing ONLY @id (or @id + minor) appearing under ref-prop
                if (
                    parent_key in _REF_PROPS216
                    and "@id" in node
                    and "@type" not in node
                    and isinstance(node.get("@id"), str)
                ):
                    _ref_ids216.append((parent_key, node["@id"]))
                for k, v in node.items():
                    if isinstance(v, list):
                        for item in v:
                            _walk216(item, k)
                    else:
                        _walk216(v, k)
            elif isinstance(node, list):
                for item in node:
                    _walk216(item, parent_key)
        for _blk in _blocks216:
            try:
                _data216 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            _walk216(_data216)
        _dangling216 = [
            f"{_prop}:{_rid}" for _prop, _rid in _ref_ids216
            if _rid not in _defined_ids216
        ]
        _ok216 = len(_ref_ids216) > 0 and not _dangling216
        check(
            _ok216,
            f"Check 216: JSON-LD 参照 @id {len(_ref_ids216)} 件全て graph 内 defined @id ({len(_defined_ids216)} 個) に解決",
            (f"Check 216: dangling @id 参照: {_dangling216!r} — entity graph が断片化し "
             "AI/知識グラフが dead anchor を踏む。参照先 node を JSON-LD 内に定義するか参照を訂正せよ"
             if _dangling216 else
             "Check 216: JSON-LD 参照 @id 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 216: index.html present",
              "Check 216: index.html が無い", blocking=True)

    # ── 217. JSON-LD @id definitions are unique within each @graph (BLOCKING) ─────
    # index.html 静的 JSON-LD の各 `<script type=application/ld+json>` block 内の
    # top-level `@graph` 配列で、`@type` + `@id` を持つ defining node が同一 @id を
    # 重複宣言しないことを BLOCKING 強制 (block を跨いだ context-redundant な Person
    # 再定義は許容)。同一 graph 内の重複は SILENT に AI/知識グラフ consumer の参照解決を
    # 非決定化。Check 216 (referential integrity) の sibling。
    _idx217 = ROOT / "index.html"
    if _idx217.exists():
        _isrc217 = _idx217.read_text(encoding="utf-8")
        _blocks217 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc217,
            flags=re.DOTALL,
        )
        from collections import Counter as _Counter217
        _all_dupes217: list[str] = []
        _total_ids217 = 0
        for _bi, _blk in enumerate(_blocks217):
            try:
                _data217 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            # top-level @graph 配列の最上位 element だけ確認 (nested embedded entities は
            # context-redundant とみなし許容)
            _graph217 = _data217.get("@graph") if isinstance(_data217, dict) else None
            if not isinstance(_graph217, list):
                continue
            _ids = []
            for _node in _graph217:
                if (
                    isinstance(_node, dict)
                    and "@type" in _node
                    and isinstance(_node.get("@id"), str)
                ):
                    _ids.append(_node["@id"])
            _total_ids217 += len(_ids)
            for _id, _n in _Counter217(_ids).items():
                if _n > 1:
                    _all_dupes217.append(f"block{_bi}:{_id}×{_n}")
        _ok217 = _total_ids217 > 0 and not _all_dupes217
        check(
            _ok217,
            f"Check 217: JSON-LD @graph top-level defining @id {_total_ids217} 件 全て block 内 unique",
            (f"Check 217: 同一 @graph 内重複 @id: {_all_dupes217!r} — AI/知識グラフが "
             "参照を非決定的に解決。同一 block 内では @id を unique へ揃えよ"
             if _all_dupes217 else
             "Check 217: JSON-LD @graph top-level defining @id 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 217: index.html present",
              "Check 217: index.html が無い", blocking=True)

    # ── 218. JSON-LD datePublished <= dateModified per node (BLOCKING) ────────────
    # index.html 静的 JSON-LD で datePublished + dateModified を両方持つ node の
    # datePublished <= dateModified を BLOCKING 強制。drift は SILENT に AI/SEO crawler
    # が "publish 前に modify された" 矛盾信号を取得し recency/trust が破壊。Check 208
    # (ISO-8601 format) の date 順序 semantic 軸版。
    from datetime import date as _date218
    _idx218 = ROOT / "index.html"
    if _idx218.exists():
        _isrc218 = _idx218.read_text(encoding="utf-8")
        _blocks218 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc218,
            flags=re.DOTALL,
        )
        _violations218: list[str] = []
        _checked_pairs218 = 0
        def _walk218(node: object, path: str) -> None:
            nonlocal _checked_pairs218
            if isinstance(node, dict):
                _dp = node.get("datePublished")
                _dm = node.get("dateModified")
                if isinstance(_dp, str) and isinstance(_dm, str):
                    try:
                        _dp_d = _date218.fromisoformat(_dp[:10])
                        _dm_d = _date218.fromisoformat(_dm[:10])
                        _checked_pairs218 += 1
                        if _dp_d > _dm_d:
                            _violations218.append(
                                f"{path}: datePublished={_dp!r} > dateModified={_dm!r}"
                            )
                    except ValueError:
                        pass  # Check 208 が format violation を担当
                for k, v in node.items():
                    _walk218(v, f"{path}.{k}")
            elif isinstance(node, list):
                for i, item in enumerate(node):
                    _walk218(item, f"{path}[{i}]")
        for _bi, _blk in enumerate(_blocks218):
            try:
                _data218 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            _walk218(_data218, f"block{_bi}")
        _ok218 = _checked_pairs218 > 0 and not _violations218
        check(
            _ok218,
            f"Check 218: JSON-LD datePublished <= dateModified — {_checked_pairs218} 件全て OK",
            (f"Check 218: 順序違反: {_violations218!r} — AI/SEO crawler が 'publish 前に "
             "modify' 矛盾信号を取得し recency/trust 破壊。datePublished <= dateModified を満たすよう揃えよ"
             if _violations218 else
             "Check 218: datePublished+dateModified 両備の node 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 218: index.html present",
              "Check 218: index.html が無い", blocking=True)

    # ── 219. aio-manifest.json paths ⊆ check_aio_digests.py MANIFEST_PATH_TO_LOCAL (BLOCKING) ─
    # aio-manifest.json の `source_of_truth` / `supporting_evidence` /
    # `observational_evidence` の全 `path` が check_aio_digests.py の
    # `MANIFEST_PATH_TO_LOCAL` dict の key に登録されていることを BLOCKING 強制。
    # 未登録 path は digest 検証されず、aio-guardian が新 evidence を manifest へ追加
    # しても check_aio_digests に登録忘れがあれば silent に digest gap が生じる。
    _mani219 = ROOT / ".well-known" / "aio-manifest.json"
    _chk_aio219 = ROOT / ".github" / "scripts" / "check_aio_digests.py"
    if _mani219.exists() and _chk_aio219.exists():
        try:
            _mdata219 = json.loads(_mani219.read_text(encoding="utf-8"))
        except json.JSONDecodeError as _e:
            _mdata219 = None
            _err219: str | None = str(_e)
        else:
            _err219 = None
        _declared219: list[str] = []
        if isinstance(_mdata219, dict):
            for _sec in ("source_of_truth", "supporting_evidence", "observational_evidence"):
                _entries = _mdata219.get(_sec, [])
                if isinstance(_entries, list):
                    for _e in _entries:
                        if isinstance(_e, dict) and isinstance(_e.get("path"), str):
                            _declared219.append(_e["path"])
        _chksrc219 = _chk_aio219.read_text(encoding="utf-8")
        # MANIFEST_PATH_TO_LOCAL 内の key 文字列を抽出 (key の literal "..."" のみ)
        _map_block219_m = re.search(
            r"MANIFEST_PATH_TO_LOCAL:[^=]*=\s*\{(.*?)\}", _chksrc219, flags=re.DOTALL
        )
        _registered219: set[str] = set()
        if _map_block219_m:
            for _km in re.finditer(r'^\s*"([^"]+)":', _map_block219_m.group(1), flags=re.M):
                _registered219.add(_km.group(1))
        _missing219 = [p for p in _declared219 if p not in _registered219]
        _ok219 = (
            _err219 is None
            and len(_declared219) > 0
            and bool(_registered219)
            and not _missing219
        )
        check(
            _ok219,
            f"Check 219: aio-manifest declared paths ({len(_declared219)} 件) 全て check_aio_digests MANIFEST_PATH_TO_LOCAL ({len(_registered219)} 件) に登録",
            (f"Check 219: 未登録 path: {_missing219!r}"
             f" / manifest parse error: {_err219!r}"
             " — check_aio_digests.py で digest 検証されず silent gap。"
             "MANIFEST_PATH_TO_LOCAL に追加せよ"),
            blocking=True,
        )
    else:
        check(False, "Check 219: aio-manifest.json + check_aio_digests.py present",
              "Check 219: aio-manifest.json もしくは check_aio_digests.py が無い", blocking=True)

    # ── 497. 静的な JSON-LD が、読む側の Check の前提の形だけで書かれていること (BLOCKING) ──
    _h497 = (ROOT / "index.html").read_text(encoding="utf-8")
    _bad497 = []
    _tags497 = [t for t in re.findall(r"<script\b[^>]*>", _h497) if "ld+json" in t.lower()]
    _bad497 += [f"script の形が違う: {t}" for t in _tags497 if t != '<script type="application/ld+json">']
    _ids497 = {}

    def _walk497(x, path):
        if isinstance(x, dict):
            if isinstance(x.get("@type"), list):
                _bad497.append(f"{path}: @type が配列")
            for _k, _v in x.items():
                if isinstance(_v, dict) and "@value" in _v:
                    _bad497.append(f"{path}/{_k}: 型付きの値 (@value)")
                _walk497(_v, f"{path}/{_k}")
            if "@id" in x and "@type" in x:
                _ids497.setdefault(x["@id"], []).append((path, x))
        elif isinstance(x, list):
            for _i, _y in enumerate(x):
                _walk497(_y, f"{path}[{_i}]")

    _blocks497 = re.findall(r'<script type="application/ld\+json">(.*?)</script>', _h497, re.S)
    for _i497, _b497 in enumerate(_blocks497):
        try:
            _walk497(json.loads(_b497), f"block{_i497}")
        except ValueError as _e497:
            _bad497.append(f"block{_i497}: JSON として読めない ({_e497})")

    def _vals497(v):
        return {json.dumps(_x, sort_keys=True, ensure_ascii=False) for _x in (v if isinstance(v, list) else [v])}

    for _id497, _nodes497 in _ids497.items():
        if len(_nodes497) < 2:
            continue
        _main497 = max(_nodes497, key=lambda n: len(n[1]))[1]
        for _p497, _n497 in _nodes497:
            for _k497, _v497 in _n497.items():
                if _k497 in ("@id", "@type") or _n497 is _main497:
                    continue
                if _k497 not in _main497 or not _vals497(_v497) <= _vals497(_main497[_k497]):
                    _bad497.append(f"{_p497}: {_id497} の {_k497} がいちばん大きいノードと食い違う")
    check(
        len(_blocks497) >= 1 and not _bad497,
        f"Check 497: 静的な JSON-LD {len(_blocks497)} 塊が、読む側の前提の形だけで書かれている (同じ @id の重複は矛盾なし)",
        (f"Check 497: 読む側の Check が読めない形の JSON-LD がある: {_bad497[:5] or 'JSON-LD の塊が無い'}。"
         "JSON-LD を読む Check は 20 を超え、どれもこの形しか読まないので、別の形は全部の Check を素通りする"),
        blocking=True,
    )
