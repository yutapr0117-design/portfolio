"""
checks_license_declaration.py — ライセンス宣言の cross-surface coherence (Check 444)

2026-11-08 に checks_license_surfaces.py から切り出した。Check の監査で 444 の面を強めた結果、
元の file が 938 行になり Check 52 の advisory 900 を超えた。444 は適用する版を名乗る全ての面
(rel=license / JSON-LD / manifest / sitemap / robots / llms / 画面 / README / REUSE.toml) を
読む塊で、他の Check と変数を共有しない。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  444. **ライセンス宣言の cross-surface coherence** (BLOCKING): 独自ライセンス ACD-1.0 が
       **機械可読な全面から一貫して発見できる**こと。444a `<link rel="license">` が index.html に
       あり実 file へ解決する / 444b JSON-LD の `license` が同一 URL を指す / 444c aio-manifest の
       top-level `license` の spdx_id と url が整合する / 444d sitemap に全文の `<loc>` がある /
       444e llms.txt と llms-full.txt が SPDX 識別子に言及する。
       **444k (2026-11-06)** 人が読む 2 面 (README の案内と画面のフッター) が、適用する版の全文を指す。
       **444n (2026-11-08)** REUSE.toml の全 file への宣言 (`path = "**"`) が適用する版であること。
       どの Check も読まず、LICENSE が 1.3 へ進んだあとも 1.0 のままだった。
       **444l / 444m (2026-11-07)** 適用する版の隣の日付がその版を確定した日である / 外向きの文書の
       「適用している版」の主張が実際の版である。確定の道具は版を置換するので、どちらも無音で偽になっていた。
       適用する版を上げる日に面を 1 つずつ戻す予行で、この 2 面だけ戻しても無音だった。
       **444h (2026-09-24)** sitemap の `<image:license>` がすべて canonical を指す —— 存在の検査は、
       矛盾する宣言の共存を検出しない（CC BY-NC-ND 4.0 が同じ画像について残っていた）。
       動機 (2026-08-23 実測): LICENSE を ACD-1.0 へ移行した時点で、**7 面すべてに宣言がゼロ**
       だった —— 「この著作物を学習に使ってよいか」に機械可読な答えが存在しなかった。
       単なる登録漏れではなく、**ACD-1.0 §6.5 自身が「自動化システムが判定できない許諾は、
       学習されるための著作物にとっては許諾ではない」と述べている**ので、本文が発見できない状態は
       ライセンスが自分の主張を満たしていないことを意味する。canonical URL は LICENSE の
       `Full text:` 行から**導出**する (決め打ちすると path を変えたとき Check だけが古い場所を
       指す)。
"""
import re
import sys
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    read = ctx.read
    extract = ctx.extract
    warnings = ctx.warnings

    # ── 444. ライセンス宣言の cross-surface coherence (BLOCKING) ────────────────────
    # 2026-08-23 実測: ACD-1.0 へ移行した時点で、機械可読な 7 面すべてに宣言がゼロだった。
    # ACD-1.0 §6.5 自身が「自動化システムが判定できない許諾は許諾ではない」と述べているので、
    # 本文が発見できない状態は**ライセンスが自分の主張を満たしていない**ことを意味する。
    # canonical URL は LICENSE の `Full text:` 行から導出する (決め打ちは path 変更時に
    # Check だけが古い場所を指す — Check 124/411/434b と同じ scope-drift)。
    import json as _json444
    _lic_decl444 = ROOT / "LICENSE"
    if not _lic_decl444.exists():
        check(False, "", "Check 444: root LICENSE が無い", blocking=True)
    else:
        _ld444 = _lic_decl444.read_text(encoding="utf-8")
        _m_path444 = re.search(r"^Full text:\s*(\S+)$", _ld444, re.M)
        _m_spdx444 = re.search(r"SPDX-License-Identifier:\s*(\S+)", _ld444)
        if not (_m_path444 and _m_spdx444):
            check(False, "", "Check 444: LICENSE から `Full text:` / SPDX 識別子を導出できない "
                             "(この 2 行は全 Check の単一ソースなので形式を保つこと)", blocking=True)
        else:
            _rel444 = _m_path444.group(1)
            _spdx444 = _m_spdx444.group(1)
            _full444 = ROOT / _rel444
            _url444 = f"https://yutapr0117-design.github.io/portfolio/{_rel444}"
            _bad444 = []

            if not _full444.exists():
                _bad444.append(f"LICENSE が指す全文 {_rel444} が存在しない")

            # 444a — HTML 標準の license リンク
            _html444 = (ROOT / "index.html").read_text(encoding="utf-8")
            # [FIX 2026-11-08] 全ての rel=license を属性の順序に依らず読み、href が適用する版を指すことを
            #   見る。旧版は先頭の 1 本が実 file へ解決するかだけを見ていたので、1.0 を指す link を
            #   先頭に置いても通った (1.0 の全文も実在するため)。
            _links444 = [_t for _t in re.findall(r"<link\b[^>]*>", re.sub(r"<!--.*?-->", "", _html444, flags=re.S))
                         if re.search(r'\brel\s*=\s*["\']license["\']', _t)]
            _hrefs444 = [(re.search(r'\bhref\s*=\s*["\']([^"\']+)["\']', _t) or [None, ""])[1] for _t in _links444]
            if not _hrefs444:
                _bad444.append("444a: index.html に rel=license の link が無い")
            for _h444 in _hrefs444:
                if _h444.lstrip("/").replace("portfolio/", "", 1) != _rel444:
                    _bad444.append(f"444a: rel=license の href {_h444!r} が適用する版の全文 /portfolio/{_rel444} を指さない")

            # 444b — JSON-LD: **CreativeWork 系ノードはすべて** license を持ち、値が canonical と一致すること。
            #   旧版は「存在する license 値が canonical と一致するか」しか見ておらず、
            #   **license を持たない CreativeWork ノードを素通し**していた。実測 (2026-08-23):
            #   ImageObject / AudioObject (バイナリ資産・XMP と ID3 は ACD-1.0 と言っている) /
            #   TechArticle / FAQPage の 6 ノードが無宣言で、**同じ資産について面ごとに答えが違う**
            #   状態だった。schema.org で `license` は CreativeWork に定義されるので、その族を対象にする
            #   (Person / Organization / BreadcrumbList は CreativeWork ではないので対象外)。
            _CW444 = {"CreativeWork", "WebSite", "WebPage", "ImageObject", "AudioObject",
                      "VideoObject", "TechArticle", "Article", "FAQPage", "MediaObject",
                      "Dataset", "SoftwareApplication", "DigitalDocument"}
            # 入れ子のノードも歩く (2026-11-11・監査 #155 / #166)。@graph の直下しか見ないと、_CW444 が挙げる
            #   MediaObject は TechArticle の encoding (llms.txt / llms-full.txt) にしか無いので対象が 0 件で、
            #   Person.subjectOf の DigitalDocument (docs/evidence の調査記録) も見なかった。入れ子で license を
            #   求めるのは、識別する URL (@id / url / contentUrl) がこのサイトのものだけ —— Zenn に載る記事
            #   (Article 22 件) や著者として名指す AI (SoftwareApplication) はこの Dedication の作品ではない
            _site444 = "https://yutapr0117-design.github.io/portfolio/"
            _ld_urls444 = set()
            _no_lic444 = []

            def _walk444(_n, _top):
                if isinstance(_n, list):
                    for _x in _n:
                        _walk444(_x, False)
                    return
                if not isinstance(_n, dict):
                    return
                _ts = [_x for _x in (_n.get("@type") if isinstance(_n.get("@type"), list) else [_n.get("@type")])
                       if isinstance(_x, str)]
                _own = any(str(_n.get(_k, "")).startswith(_site444) for _k in ("@id", "url", "contentUrl"))
                if set(_ts) & _CW444 and (_top or (_own and set(_n) - {"@id", "@type"})):
                    if "license" in _n:
                        _ld_urls444.add(_n["license"])
                    else:
                        _no_lic444.append(f"{'/'.join(_ts)} {_n.get('@id') or _n.get('contentUrl') or _n.get('url') or '(no @id)'}")
                for _k, _v in _n.items():
                    if _k != "license":
                        _walk444(_v, False)

            for _blk444 in re.findall(
                    r'<script type="application/ld\+json">(.*?)</script>', _html444, re.S):
                try:
                    _doc444 = _json444.loads(_blk444)
                except Exception:
                    continue
                for _n444 in (_doc444.get("@graph") or [_doc444]):
                    _walk444(_n444, True)
            if not _ld_urls444:
                _bad444.append("JSON-LD にどの CreativeWork ノードも license を持たない")
            if _no_lic444:
                _bad444.append(f"license を持たない CreativeWork ノード: {_no_lic444}")
            if _ld_urls444 and _ld_urls444 != {_url444}:
                _bad444.append(f"JSON-LD の license が canonical と不一致: {sorted(_ld_urls444)} != {_url444}")

            # 444f — **runtime で注入される JSON-LD** にも license が載ること。
            #   静的側だけ配線すると、route 追従ノード (#webpage-dynamic) は別 @id なので
            #   **そのノードだけ許諾不明**になる (レンダリングするクローラが読むのはこちら)。
            #   実装は shipped JS にあるので、**直接リテラル**か **SITE_CONFIG.LICENSE_URL 経由**の
            #   どちらかで参照していることを見る (間接参照の方が単一ソースとして優れているので、
            #   リテラルだけを要求すると**正しい実装を誤検出する** —— 初版で実際に踏んだ)。
            #   間接参照を許す代わり、SITE_CONFIG.LICENSE_URL の定義値が canonical と一致することを
            #   別途確かめる (そうしないと「どこかを指してはいるが別物」を素通しする)。
            _mainjs444 = (ROOT / "main.js").read_text(encoding="utf-8")
            _m_lu444 = re.search(r"LICENSE_URL:\s*'([^']+)'", _mainjs444)
            if not _m_lu444:
                _bad444.append("main.js の SITE_CONFIG に LICENSE_URL が無い")
            elif _m_lu444.group(1) != _url444:
                _bad444.append(f"SITE_CONFIG.LICENSE_URL {_m_lu444.group(1)!r} != canonical {_url444!r}")
            # [FIX 2026-11-08] JSON-LD の `license` の値そのものを見る。旧版は file 全文に全文の path か
            #   SITE_CONFIG.LICENSE_URL が在るかだけを見ていて、SITE_CONFIG の定義行が常に満たしたので、
            #   ノードの値を別の版にしても、行を消しても通った。
            from _lib_io import strip_js_comments as _strip444f
            for _f444, _label444 in ((ROOT / "main.js", "route 追従ノード (#webpage-dynamic)"),
                                     (ROOT / "js" / "meta-management.js", "speakable ノード")):
                _src444 = _strip444f(_f444.read_text(encoding="utf-8"))
                _vals444 = re.findall(r"""['"]license['"]\s*:\s*([^,\n}]+)""", _src444)
                if not _vals444:
                    _bad444.append(f"444f: {_f444.name} の {_label444} が JSON-LD に license を宣言していない")
                for _v444 in _vals444:
                    if "SITE_CONFIG.LICENSE_URL" not in _v444 and _rel444 not in _v444:
                        _bad444.append(f"444f: {_f444.name} の {_label444} の license が適用する版を指さない: {_v444.strip()[:80]}")

            # 444c — aio-manifest の license 宣言
            _mf444 = ROOT / ".well-known" / "aio-manifest.json"
            try:
                _mj444 = _json444.loads(_mf444.read_text(encoding="utf-8"))
            except Exception:
                _mj444 = {}
            _lo444 = _mj444.get("license")
            if not isinstance(_lo444, dict):
                _bad444.append("aio-manifest.json に top-level license オブジェクトが無い")
            else:
                if _lo444.get("spdx_id") != _spdx444:
                    _bad444.append(f"manifest の spdx_id {_lo444.get('spdx_id')!r} != LICENSE の {_spdx444!r}")
                if _lo444.get("url") != _url444:
                    _bad444.append(f"manifest の license.url が canonical と不一致: {_lo444.get('url')!r}")
                # 同じブロックの SPDX 式と名前も同じ版を述べること (2026-11-08: 旧版は 2 つを比べず、
                #   1.0 へ戻しても通った)
                if _lo444.get("conforming_spdx_expression") != f"LicenseRef-{_spdx444}":
                    _bad444.append(f"444c: manifest の conforming_spdx_expression {_lo444.get('conforming_spdx_expression')!r} "
                                   f"!= LicenseRef-{_spdx444}")
                if not str(_lo444.get("name", "")).endswith(" " + _spdx444.split("-", 1)[1]):
                    _bad444.append(f"444c: manifest の license.name {_lo444.get('name')!r} が {_spdx444} の版を述べない")

            # 444d — sitemap から全文へ到達できること
            _sm444 = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
            # 照合は <loc> の値の完全一致で行う (コメントは除く)。2026-11-02 まで sitemap 全文の
            # 部分文字列で見ており、全文の <url> を丸ごと消しても、画像の
            # `<image:license>` (444h が同じ URL であることを要求する) と説明コメントが同じ URL を
            # 持つので緑のままだった (Check 132 と同じ class)。
            _locs444 = set(re.findall(
                r"<loc>\s*([^<\s]+)\s*</loc>", re.sub(r"<!--.*?-->", "", _sm444, flags=re.S)))
            if _url444 not in _locs444:
                _bad444.append(f"sitemap.xml に {_rel444} の <loc> が無い (crawler が到達できない)")

            # 444h — sitemap の画像ライセンス宣言が canonical と食い違わないこと。
            # 444d は「在ること」しか見ておらず、同じ画像について XMP と JSON-LD が ACD-1.0 を
            # 述べる横で `<image:license>` が CC BY-NC-ND 4.0 を宣言し続けていた (2026-09-24 発見)。
            # **存在の検査は、矛盾する宣言の共存を検出しない。**
            # 値の取り方は `[^<\s]+` ではなく `(.*?)` + re.S + strip にしてある。
            # **差は実測した** (2026-09-24): 折り返した URL は前者でも拾える (周囲の `\s*` が吸う) が、
            # **空白を含む値 `CC BY-NC-ND 4.0` と空要素は一致 0 件になり、黙って通る** ——
            # 人間が手で書けばライセンス*名*を書く方が自然なので、これは現実に起こる形である。
            # **一致が 0 件であることは「違反が無い」と区別がつかない。**
            _ils444 = re.findall(r"<image:license>\s*(.*?)\s*</image:license>", _sm444, re.S)
            if not _ils444:  # 0 件は「違反が無い」と区別がつかない (2026-11-08 まで else が無かった)
                _bad444.append("444h: sitemap.xml に <image:license> が 1 件も無い (画像のライセンス宣言が消えた)")
            for _il444 in _ils444:
                if _il444.strip() != _url444:
                    _bad444.append(f"444h: sitemap.xml の <image:license> が canonical と異なるライセンスを宣言: {_il444.strip()}")

            # 444d (robots) — 全文と記述子が、どの bot の group でも Disallow されていないこと (RFC 9309)。
            #   名前付きの group を持つ bot は `*` の group を読まないので、Allow の和集合では見えない
            #   (GPTBot の group で LICENSES/ を拒否しても `*` の Allow が満たしていた・2026-11-08)。
            from _lib_io import parse_robots_groups as _groups444d
            _grp444d = [g for g in _groups444d((ROOT / "robots.txt").read_text(encoding="utf-8")) if g[0]]

            def _allowed444d(_agent, _path):
                _mine = [r for a_, r in _grp444d if _agent in a_] or [r for a_, r in _grp444d if "*" in a_]
                _best = (-1, True)
                for _rules in _mine:
                    for _k, _v in _rules:
                        if not _v:
                            continue
                        _rx = "^" + re.escape(_v).replace(r"\*", ".*").replace(r"\$", "$")
                        if re.match(_rx, _path) and (len(_v), _k == "allow") > _best:
                            _best = (len(_v), _k == "allow")
                return _best[1]
            for _ag444d in sorted({a_ for ag, _ in _grp444d for a_ in ag}):
                for _p444d in (f"/portfolio/{_rel444}", f"/portfolio/{_rel444[:-4]}.machine.json"):
                    if not _allowed444d(_ag444d, _p444d):
                        _bad444.append(f"444d: robots.txt の User-agent: {_ag444d} の group が {_p444d} を拒否している")

            # 444k — 人が読む面が適用する版を指すこと。README と画面のフッターは機械可読面ではないので
            #   444a〜444h の外にあり、適用する版を上げる日に戻しても無音だった (2026-11-06 の予行)。
            _rd444k = (ROOT / "README.md").read_text(encoding="utf-8")
            if f"]({_rel444})" not in _rd444k:
                _bad444.append(f"444k: README.md が適用する版の全文 {_rel444} へリンクしていない")
            # ACD-1.0 を常に許していたので、英語節のリンクを 1.0 へ戻しても日本語節が満たした (2026-11-08 の監査)
            _stale444k = sorted({_v for _v in re.findall(r"LICENSES/(ACD-\d+\.\d+)\.txt", _rd444k)} - {_spdx444})
            if _stale444k:
                _bad444.append(f"444k: README.md が適用していない版の本文を案内している: {_stale444k}")
            _says444k = re.findall(r"this repository applies (?:its )?(?:frozen )?(?:successor )?(ACD-\d+\.\d+)|このリポジトリのライセンス（(ACD-\d+\.\d+)",
                                  " ".join(re.sub(r"(?m)^>\s?", "", _rd444k).split()))  # 引用の折り返しをまたいで読む
            if len(_says444k) < 2 or any((_a or _b) != _spdx444 for _a, _b in _says444k):
                _bad444.append(f"444k: README.md の英日 2 つの宣言の文が適用する版 {_spdx444} を述べていない: {[_a or _b for _a, _b in _says444k]}")
            # コメントを除いてから見る。フッターをリンクごとコメントにすると画面から消えるのに、
            #   素の `in` ではコメントの中の URL で通っていた (2026-11-08 の監査で実測)。
            from _lib_io import strip_js_comments as _strip444k
            _cp444k = _strip444k((ROOT / "js" / "components.js").read_text(encoding="utf-8"))
            if f"/portfolio/{_rel444}" not in _cp444k or f"License: {_spdx444}" not in _cp444k:
                _bad444.append(f"444k: 画面のフッター (js/components.js) が適用する版 {_spdx444} を指していない")

            # 444o — 版を述べるのに、どの面にも読まれていなかった 3 面 (2026-11-09・Check の監査 #159): index.html の
            #   RAG 抽出用の `Licence:` の行と、.well-known の 2 つの index.json の skill の description
            #   (`licensing (ACD-x.y: …)`)。どちらも 1.0 へ戻しても緑だった。確定の道具は版を置換する
            _ft444o = re.findall(r"Licence:\s*\S*/LICENSES/(ACD-\d+\.\d+)\.txt", (ROOT / "index.html").read_text(encoding="utf-8"))
            if not _ft444o or set(_ft444o) != {_spdx444}:
                _bad444.append(f"444o: index.html の RAG 用の Licence: 行が {_ft444o or '読めない'} を指し、適用する版 {_spdx444} と違う")
            for _ix444o in (".well-known/index.json", ".well-known/agent-skills/index.json"):
                _v444o = re.findall(r"[Ll]icensing \((ACD-\d+\.\d+):", (ROOT / _ix444o).read_text(encoding="utf-8"))
                if not _v444o or set(_v444o) != {_spdx444}:
                    _bad444.append(f"444o: {_ix444o} の skill の licensing が {_v444o or '読めない'} と述べ、適用する版 {_spdx444} と違う")

            # 444n — REUSE.toml の全 file への宣言が、適用する版であること。REUSE を読む道具はここだけを見る。
            #   どの Check も読んでいなかったので、LICENSE が 1.3 へ進んだあとも 1.0 のままだった
            #   (2026-09-23〜2026-11-08。2026-11-08 の監査で発見)。
            _ru444n = re.search(r'path = "\*\*"[^\[]*?SPDX-License-Identifier = "([^"]+)"',
                                (ROOT / "REUSE.toml").read_text(encoding="utf-8"), re.S)
            if not _ru444n or _ru444n.group(1) != f"LicenseRef-{_spdx444}":
                _bad444.append(f"444n: REUSE.toml の path = \"**\" が {_ru444n.group(1) if _ru444n else '読めない'} "
                               f"と宣言し、適用する版 LicenseRef-{_spdx444} と食い違う")

            # 444l — 適用する版の隣の日付が、その版を確定した日であること。版を置換しても日付は残るので、
            #   "ACD-1.4 (ACD-1.0 until 2026-10-25)" のように公開面が偽を述べても無音だった (2026-11-07 の予行)。
            _ptr444l = re.search(r"frozen on (\d{4}-\d{2}-\d{2})", " ".join((ROOT / "LICENSES" / f"{_spdx444}-DRAFT.txt").read_text(encoding="utf-8").split()))
            if not _ptr444l:
                _bad444.append(f"444l: {_spdx444} を確定した日が草案の pointer から読めない")
            else:
                for _f444l in ("README.md", "llms.txt", "llms_well-known.txt", ".well-known/llms.txt", ".well-known/llms_well-known.txt", "robots.txt", "sitemap.xml"):
                    for _l444l in (ROOT / _f444l).read_text(encoding="utf-8").splitlines():
                        if _spdx444 in _l444l:
                            _bad444 += [f"444l: {_f444l} が {_spdx444} の隣で {_d or _e} と述べる / 確定は {_ptr444l.group(1)}"
                                        for _d, _e in re.findall(r"(?:until|since) (\d{4}-\d{2}-\d{2})|(\d{4}-\d{2}-\d{2}) ?(?:まで|から)", _l444l)
                                        if (_d or _e) != _ptr444l.group(1)]

            # 444e — llms 層が識別子に言及すること
            # [FIX 2026-11-08] 宣言の文 (released under the **… (ACD-x)**) の版を見る。旧版は識別子が
            #   file のどこかに 1 回あれば通り、宣言の文が別の版を述べても他の行が満たした。
            #   LICENSE 本文の同じ文も見る。名前の版 (Dedication 1.3) も識別子と同じ版であること (2026-11-08 の監査)
            for _lf444 in ("llms.txt", "llms-full.txt", "llms_well-known.txt", ".well-known/llms.txt", "LICENSE"):
                _lt444 = " ".join((ROOT / _lf444).read_text(encoding="utf-8").split())
                _decl444 = [f"ACD-{_v}" if f"ACD-{_v}" == _i else f"{_i} (名前は {_v})" for _v, _i in re.findall(
                    r"released under the \**Autonomous Commons Dedication ([\d.]+) \((ACD-[\d.]+)\)", _lt444)]
                if not _decl444:
                    _bad444.append(f"444e: {_lf444} にライセンスの宣言の文 (released under the …) が無い")
                elif set(_decl444) != {_spdx444}:
                    _bad444.append(f"444e: {_lf444} の宣言の文が {sorted(set(_decl444))} と述べ、適用する版 {_spdx444} と違う")

            # 444g — **機械可読記述子**が discovery 面から到達できること。
            # 記述子 (`LICENSES/ACD-1.0.machine.json`) は「SPDX 識別子だけでは機械学習可否も
            # 特許許諾も判定できない」という穴を埋めるために置いた面で、**置いただけで
            # sitemap / robots / manifest から辿れなければ §6.5 が空になる** (本文について
            # 2026-08-23 に起きたのと同じ class)。存在するときだけ 3 面を検証する。
            # 2026-10-25: 記述子の path も LICENSE の `Full text:` から導出する (1.0 決め打ちだったため、
            # 適用する版を 1.3 へ切り替えた日に、manifest が正しく 1.3 の記述子を指しているのを誤検出した)。
            _mrel444 = _rel444[:-len(".txt")] + ".machine.json" if _rel444.endswith(".txt") else _rel444
            _md444 = ROOT / _mrel444
            if _md444.exists():
                _murl444 = _url444.replace(_rel444, _mrel444)
                if _murl444 not in _locs444:
                    _bad444.append(f"sitemap.xml に {_mrel444} の <loc> が無い (記述子へ到達できない)")
                # robots は Allow rule の値で見る (コメント中の path 言及では満たされない)
                from _lib_io import parse_robots_groups as _groups444
                _allow444 = {
                    _v.lstrip("/") for _ag, _rules in _groups444(
                        (ROOT / "robots.txt").read_text(encoding="utf-8"))
                    for _k, _v in _rules if _k == "allow"
                }
                if not ({_mrel444, "portfolio/" + _mrel444} & _allow444):
                    _bad444.append(f"robots.txt が {_mrel444} を Allow していない")
                try:
                    _mlic444 = _json444.loads(
                        (ROOT / ".well-known" / "aio-manifest.json").read_text(encoding="utf-8")
                    ).get("license", {})
                except ValueError:
                    _mlic444 = {}
                if _mlic444.get("machine_readable") != _murl444:
                    _bad444.append(
                        "aio-manifest の license.machine_readable が記述子を指していない "
                        f"({_mlic444.get('machine_readable')!r})")

            check(
                not _bad444,
                f"Check 444 (444a rel=license / 444b JSON-LD / 444c manifest / 444d sitemap / "
                f"444e llms / 444f runtime JSON-LD / 444g 記述子の到達性 / 444h 画像ライセンスの矛盾): "
                f"ライセンス宣言が全機械可読面で整合 ({_spdx444} / {_rel444})",
                (f"Check 444: ライセンス宣言の cross-surface drift: {_bad444}。"
                 "**ACD-1.0 §6.5 は「自動化システムが判定できない許諾は許諾ではない」と述べている** —— "
                 "どこか 1 面でも欠けると、その経路の agent は「学習してよいか」を判定できない。"
                 "canonical は LICENSE の `Full text:` 行と `SPDX-License-Identifier:` 行が単一ソース"),
                blocking=True,
            )

    # 444m — 外向きの文書の「適用している版」の主張が、実際に適用している版であること。確定の道具が書き換えるのは
    #   機械可読面だけなので、REVIEWERS.md の "ACD-1.3 is the one this repository applies" は版を上げても残る。
    _lic444m = re.search(r"^SPDX-License-Identifier:\s*(\S+)", (ROOT / "LICENSE").read_text(encoding="utf-8"), re.M)
    if _lic444m:
        from measure_citation_drift import FACES as _faces444m
        _say444m = re.compile(r"(?i)\b(?:this|the) repository applies|(?:applied|applies) to this repository|適用している|適用中")
        _id444m = re.compile(r"ACD-\d+\.\d+(?![.\w-]*\.md)|(?<![\w§.])1\.\d+(?=\s*を適用)")
        _stale444m, _free444m, _exm444m = [], [], []
        for _f444m in [ROOT / "LICENSES" / _n for _n in _faces444m if "against" not in _n and "discussion-log" not in _n]:
            # 段落 (表の行は 1 行ずつ) を単位にし、版は主張と同じ文の中で最も近いものを見る (2026-11-08: 行の
            #   70 字の窓は、折り返した段落の前の行の版を見ず、版の無い主張は黙って通っていた・aa の提案)
            _para444m, _buf444m = [], []
            for _n444m, _l444m in enumerate(_f444m.read_text(encoding="utf-8").splitlines() + [""], 1):
                _t444m = re.sub(r"^\s*>\s?", "", _l444m)
                if _buf444m and (not _t444m.strip() or _t444m.lstrip().startswith("|") or _buf444m[0][1].lstrip().startswith("|")):
                    _para444m.append((_buf444m[0][0], " ".join(_x for _, _x in _buf444m)))
                    _buf444m = []
                if _t444m.strip():
                    _buf444m.append((_n444m, _t444m.strip()))
            for _n444m, _p444m in _para444m:
                for _m444m in _say444m.finditer(_p444m):
                    _st = max([_x.end() for _x in re.finditer(r"[.?!] |。", _p444m[:_m444m.start()])], default=0)
                    _en = next((_m444m.end() + _x.start() for _x in re.finditer(r"[.?!] |。", _p444m[_m444m.end():])), len(_p444m))
                    _sent = _p444m[_st:_en]
                    if re.search(r"(?i)\bnot\s*$", _p444m[_st:_m444m.start()].replace("*", "").rstrip() + " ") or \
                            re.search(r"(?i)\bnot\b[^.]{0,12}$", _p444m[_st:_m444m.start()].replace("*", "")):
                        continue  # 否定文 ("is **not** applied to this repository") は主張ではない
                    if _m444m.group(0).startswith("適用") and "このリポジトリ" not in _sent:
                        continue  # 日本語は「このリポジトリ」の文だけを主張と読む (FAQ の「全貢献者が適用している」は別の意味)
                    _hit444m = min((_i for _i in _id444m.finditer(_p444m) if _st <= _i.start() < _en),
                                   key=lambda _i: abs(_i.start() - _m444m.start()), default=None)
                    if _hit444m is None:
                        # 版の無い主張は RED。免除は 2 つの語の形だけ (aa の判断・2026-11-08): 主語が族の名前の
                        #   "ACD"（版を書くと「その版の採用」へ狭まる）と、版を LICENSE に委ねる案内 "names the version"
                        _exempt444m = (re.search(r"\bACD\b(?!-\d)[^.]{0,20}$", _p444m[_st:_m444m.start()])
                                       or "names the version" in _sent)
                        (_exm444m if _exempt444m else _free444m).append(f"{_f444m.name}:{_n444m}")
                    elif "ACD-" + _hit444m.group(0).removeprefix("ACD-") != _lic444m.group(1):
                        _stale444m.append(f"{_f444m.name}:{_n444m}")
        check(
            not _stale444m and not _free444m,
            (f"Check 444m: 外向きの文書の「適用している版」の主張が {_lic444m.group(1)} に合う "
             f"(版の無い主張は免除の形の {len(_exm444m)} 件だけ: {sorted(set(_exm444m))})"),
            (f"Check 444m: 適用していない版を「適用している」と述べる行 {sorted(set(_stale444m))} / 同じ文に版の無い主張 "
             f"{sorted(set(_free444m))}。文を読んで直す (版を書くか、族の名前 ACD を主語にするか、版を LICENSE に委ねる案内にする)"),
            blocking=True,
        )
