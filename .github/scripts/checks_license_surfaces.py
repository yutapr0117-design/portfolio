"""
checks_license_surfaces.py — ライセンスの機械可読面と凍結の Check 群 (444 / 445 / 451 / 452 / 453)
(2026-10-26 に checks_aio_config.py から切り出した — 980 行で Check 52 の advisory 950 を超え、
1,000 行の BLOCKING (Check 365) まで 20 行だった。OSI の作業で最も触る検査なので、止まる前に分けた)。

444 ライセンス宣言の cross-surface coherence / 445 SPDX 提出用 XML の同期 / 451 機械可読記述子と条文 /
452 提出準備マーカー / 453 凍結中の提出物。いずれも自前で対象 file を読み、checks_aio_config.py の
他の Check (62-69) と変数を共有しない。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  444. **ライセンス宣言の cross-surface coherence** (BLOCKING): 独自ライセンス ACD-1.0 が
       **機械可読な全面から一貫して発見できる**こと。444a `<link rel="license">` が index.html に
       あり実 file へ解決する / 444b JSON-LD の `license` が同一 URL を指す / 444c aio-manifest の
       top-level `license` の spdx_id と url が整合する / 444d sitemap に全文の `<loc>` がある /
       444e llms.txt と llms-full.txt が SPDX 識別子に言及する。
       **444h (2026-09-24)** sitemap の `<image:license>` がすべて canonical を指す —— 存在の検査は、
       矛盾する宣言の共存を検出しない（CC BY-NC-ND 4.0 が同じ画像について残っていた）。
       動機 (2026-08-23 実測): LICENSE を ACD-1.0 へ移行した時点で、**7 面すべてに宣言がゼロ**
       だった —— 「この著作物を学習に使ってよいか」に機械可読な答えが存在しなかった。
       単なる登録漏れではなく、**ACD-1.0 §6.5 自身が「自動化システムが判定できない許諾は、
       学習されるための著作物にとっては許諾ではない」と述べている**ので、本文が発見できない状態は
       ライセンスが自分の主張を満たしていないことを意味する。canonical URL は LICENSE の
       `Full text:` 行から**導出**する (決め打ちすると path を変えたとき Check だけが古い場所を
       指す)。
  445. **SPDX 提出用 XML がライセンス本文と同期していること** (BLOCKING): SPDX License List への
       収録が受理されると提出者は **XML とテストテキストの作成**を求められる。その XML を手書きすると
       **本文を改善するたび silent に古くなる** —— しかも XML は普段誰も読まないので drift に
       気付く経路が無い (本リポジトリが繰り返し潰してきた「宣言はあるが実態が伴わない」class)。
       `LICENSES/ACD-1.0.txt` を単一ソースとして `generate_spdx_license_xml.py` が導出し、
       本 Check が「再生成して一致するか」を検証する (STATUS.md に対する Check 121 と同じ設計)。
       445a XML が本文から再生成した結果と byte 一致する / 445b XML が well-formed で
       licenseId が LICENSE の SPDX 識別子と一致する / 445c 本文の全条項番号が XML に現れる
       (段落分割で条項が落ちていない —— 提出テキストと配布テキストが食い違うと収録後に
       「テキストが一致しない」問題を起こす)。
  451. ACD-1.0 の機械可読記述子 (`LICENSES/ACD-1.0.machine.json`) が条文と整合すること。
       451d: 1.0 以外の版の記述子 (`ACD-<ver>.machine.json`) も、それぞれの版の本文と整合すること (2026-10-17)。
       ACD-1.0 §6.5 は「自動化されたシステムが判定できない許諾は、学習されるための著作物に
       とっては許諾ではない」と述べる。そう述べるライセンス自身が機械から判定できないのは
       自己矛盾なので、採用者がそのままコピーできる非 operative の記述子を置いている。
       ただし second source of truth は必ず drift するので 3 面を BLOCKING で縛る:
       451a = 記述子が引く clause 番号がすべて本文に実在する (記述子は要約ではなく**索引**
       なので、番号がずれた時点で「根拠を辿れる」という唯一の価値が消える)。
       451b = 記述子の notice が §16.1 の通知文と一致する (二重管理すると、片方だけ更新した
       瞬間に**採用者が古い通知を貼る**)。451c = 公開 manifest の license boolean と食い違わ
       ない (判定する側はどちらか一方しか読まないので、食い違いは片方の読み手を確実に誤らせる
       —— C6 の「全公開面で食い違わない」の license 面)。3 部それぞれ単独で RED を実測済。
       (BLOCKING)

  452. 提出準備マーカー `LICENSES/READY-TO-SUBMIT.md` が実態と一致すること。マーカーは
       「ACD-1.0 がレビュー結果を見たいと思える水準に達した」という判断を **ファイルの存在**
       で表す成果物で、`ACD-1.0.submission.md` が「これが無い限り送るな」と参照している。
       **マーカーは腐ると最も危険な文書**である —— 条文を改訂したあと数値が古いままだと、
       読み手は「達した」という判断を **別のテキストについて** 読むことになる。存在するときだけ、
       主張する実測値 (節数 / 項数 / 行数) が本文と一致することと、**文中から導出した**参照先が
       すべて実在することを検証する。参照先をハードコード一覧の「文中に現れたら見る」形にすると、
       **参照を別の名前へ書き換えた瞬間に検査対象から外れる** (非 vacuity 検証で実測)。
       判断そのものを撤回するならファイルを削除するのが正しい。 (BLOCKING)

  453. 凍結中のライセンス提出物が動かないこと。2026-08-24、オーナーが SPDX / OSI へ申請する
       ため「結果を伝えるまでライセンスをそのままにしておいてほしい」と述べた。**「触らない」を
       記憶や善意に委ねない** —— このリポジトリは AI が無限に自走する前提で動いており、次の
       セッションの担当はその会話を見ていない。凍結を git 上の成果物 (`LICENSES/FROZEN.md`) に
       して BLOCKING で縛れば、うっかり触った時点で CI が赤くなる。存在するときだけ有効で、
       解除は FROZEN.md の削除で表す。**回避の抑止**として、sha256 の一致だけでなく**凍結対象
       path の集合**も検証する (対象を表から外せば Check は黙るが、それは実質的な解除である)。
       本文に欠陥を見つけたときの正しい行動は、直すことではなく**オーナーへ報告すること**
       (審査中の差し替えは、審査側が見ているテキストとの乖離を生む)。 (BLOCKING)
"""
import re
import sys
import json
import xml.etree.ElementTree as ET


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
            _m_link444 = re.search(r'<link\s+rel="license"\s+href="([^"]+)"', _html444)
            if not _m_link444:
                _bad444.append("index.html に rel=license の link が無い")
            elif not (ROOT / _m_link444.group(1).lstrip("/").replace("portfolio/", "", 1)).exists():
                _bad444.append(f"rel=license の href {_m_link444.group(1)} が実 file へ解決しない")

            # 444b — JSON-LD: **CreativeWork 系ノードはすべて** license を持ち、値が canonical と一致すること。
            #   旧版は「存在する license 値が canonical と一致するか」しか見ておらず、
            #   **license を持たない CreativeWork ノードを素通し**していた。実測 (2026-08-23):
            #   ImageObject / AudioObject (バイナリ資産・XMP と ID3 は ACD-1.0 と言っている) /
            #   TechArticle / FAQPage の 6 ノードが無宣言で、**同じ資産について面ごとに答えが違う**
            #   状態だった。schema.org で `license` は CreativeWork に定義されるので、その族を対象にする
            #   (Person / Organization / BreadcrumbList は CreativeWork ではないので対象外)。
            _CW444 = {"CreativeWork", "WebSite", "WebPage", "ImageObject", "AudioObject",
                      "VideoObject", "TechArticle", "Article", "FAQPage", "MediaObject",
                      "Dataset", "SoftwareApplication"}
            _ld_urls444 = set()
            _no_lic444 = []
            for _blk444 in re.findall(
                    r'<script type="application/ld\+json">(.*?)</script>', _html444, re.S):
                try:
                    _doc444 = _json444.loads(_blk444)
                except Exception:
                    continue
                for _n444 in (_doc444.get("@graph") or [_doc444]):
                    if not isinstance(_n444, dict) or _n444.get("@type") not in _CW444:
                        continue
                    if "license" in _n444:
                        _ld_urls444.add(_n444["license"])
                    else:
                        _no_lic444.append(f"{_n444.get('@type')} {_n444.get('@id', '(no @id)')}")
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
            for _f444, _label444 in ((ROOT / "main.js", "route 追従ノード (#webpage-dynamic)"),
                                     (ROOT / "js" / "meta-management.js", "speakable ノード")):
                _src444 = _f444.read_text(encoding="utf-8")
                if _rel444 not in _src444 and "SITE_CONFIG.LICENSE_URL" not in _src444:
                    _bad444.append(f"{_f444.name} の {_label444} が license を宣言していない "
                                   f"({_rel444} のリテラルも SITE_CONFIG.LICENSE_URL 参照も無い)")

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

            # 444d — sitemap から全文へ到達できること
            _sm444 = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
            if _url444 not in _sm444:
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
            for _il444 in re.findall(r"<image:license>\s*(.*?)\s*</image:license>", _sm444, re.S):
                if _il444.strip() != _url444:
                    _bad444.append(f"sitemap.xml の <image:license> が canonical と異なるライセンスを宣言: {_il444.strip()}")

            # 444e — llms 層が識別子に言及すること
            for _lf444 in ("llms.txt", "llms-full.txt"):
                if _spdx444 not in (ROOT / _lf444).read_text(encoding="utf-8"):
                    _bad444.append(f"{_lf444} が {_spdx444} に言及していない")

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
                if _murl444 not in _sm444:
                    _bad444.append(f"sitemap.xml に {_mrel444} の <loc> が無い (記述子へ到達できない)")
                _rb444 = (ROOT / "robots.txt").read_text(encoding="utf-8")
                if _mrel444 not in _rb444:
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

    # ── 445. SPDX 提出用 XML がライセンス本文と同期していること (BLOCKING) ─────────────
    # 提出物を手書きすると本文の改善に追従せず silent に古くなる。単一ソース (ACD-1.0.txt) から
    # 導出し、ここで「再生成して一致するか」を検証する (Check 121 と同じ regenerate-compare)。
    import subprocess as _sp445
    import xml.etree.ElementTree as _ET445
    _xml445 = ROOT / "LICENSES" / "ACD-1.0.spdx.xml"
    _gen445 = ROOT / ".github" / "scripts" / "generate_spdx_license_xml.py"
    if not (_xml445.exists() and _gen445.exists()):
        check(False, "", f"Check 445: SPDX 提出物または生成器が無い "
                         f"(xml={_xml445.exists()} / generator={_gen445.exists()})", blocking=True)
    else:
        # 445a — 再生成して一致するか
        _r445 = _sp445.run([sys.executable, str(_gen445), "--check"],
                           cwd=str(ROOT), capture_output=True, text=True)
        check(
            _r445.returncode == 0,
            "Check 445a: SPDX 提出用 XML が ACD-1.0 本文と同期している",
            (f"Check 445a: SPDX 提出用 XML が本文と同期していない — `npm run spdx-xml` を実行して "
             f"commit せよ。**提出物は手で編集しない** (単一ソースは LICENSES/ACD-1.0.txt)。"
             f"詳細: {_r445.stdout.strip() or _r445.stderr.strip()}"),
            blocking=True,
        )

        # 445b — well-formed かつ識別子が**出典の本文 (ACD-1.0.txt) の版**と一致
        #   2026-10-25 までは LICENSE の識別子と照合していたが、適用する版を 1.3 へ切り替えた日に
        #   「1.0 の提出物が 1.0 を名乗っている」正しい状態を誤検出した。XML は凍結された 1.0 の提出物で、
        #   照合すべきは**それが導出された本文**である。
        _bad445 = []
        try:
            _root445 = _ET445.fromstring(_xml445.read_text(encoding="utf-8"))
            _lic445 = _root445.find("{http://www.spdx.org/license}license")
            if _lic445 is None:
                _bad445.append("license 要素が無い")
            else:
                _src_id445 = re.sub(r"\.spdx\.xml$", "", _xml445.name)
                if _lic445.get("licenseId") != _src_id445:
                    _bad445.append(f"licenseId {_lic445.get('licenseId')!r} != 出典の版 {_src_id445!r}")
        except Exception as _e445:
            _bad445.append(f"XML が well-formed でない: {_e445}")
        check(
            not _bad445,
            "Check 445b: SPDX 提出用 XML が well-formed で識別子が出典の版と一致",
            f"Check 445b: SPDX 提出物の構造/識別子に問題がある: {_bad445}",
            blocking=True,
        )

        # 445c — 本文の全条項が XML に現れる (段落分割で落ちていない)
        _src445 = (ROOT / "LICENSES" / "ACD-1.0.txt").read_text(encoding="utf-8")
        _clauses445 = re.findall(r"^  (\d+\.\d+)\s", _src445, re.M)
        try:
            _joined445 = " ".join(
                (_p.text or "") for _p in
                _ET445.fromstring(_xml445.read_text(encoding="utf-8"))
                .findall(".//{http://www.spdx.org/license}p"))
        except Exception:
            _joined445 = ""
        _miss445 = [_c for _c in _clauses445 if _c not in _joined445]
        check(
            _clauses445 and not _miss445,
            f"Check 445c: 本文の全 {len(_clauses445)} 条項が SPDX 提出用 XML に現れる",
            (f"Check 445c: SPDX 提出用 XML に現れない条項がある: {_miss445[:8]}。"
             "**提出テキストと配布テキストが食い違うと、収録後に「テキストが一致しない」問題を起こす**。"
             "生成器の段落分割ロジックを見直せ"),
            blocking=True,
        )

        # 445d — 段落の先頭に立つ条項番号が、本文の条項列と **順序・個数まで一致**する。
        # [ADD 2026-08-23] 445c は「条項が *現れる*」しか見ないので、**1 つの文が 2 つの段落に
        #   割れても素通り**する (割れた後半が実在の条項番号で始まると 445b/c のどちらにも掛から
        #   ない)。実際に生成器が折り返しの継続行を新段落と誤認し、§16.5 の「…and Section」/
        #   「10.5 applies.」など **3 文が割れていた**。Check 445a の regenerate-compare も、
        #   生成器自体が壊れていれば**壊れた出力どうしが一致する**ので捕捉できない。
        #   本文の条項列 (indent 2 の `N.N `) と、XML で段落頭に立つ条項番号の列を突き合わせる。
        try:
            _ps445 = [(_p.text or "").strip() for _p in
                      _ET445.fromstring(_xml445.read_text(encoding="utf-8"))
                      .findall(".//{http://www.spdx.org/license}p")]
        except Exception:
            _ps445 = []
        _xmlseq445 = [_t.split()[0] for _t in _ps445 if re.match(r"^\d+\.\d+\s", _t)]
        _seq_ok445 = bool(_clauses445) and _xmlseq445 == _clauses445
        _extra445 = [_c for _c in _xmlseq445 if _xmlseq445.count(_c) > _clauses445.count(_c)]
        check(
            _seq_ok445,
            f"Check 445d: XML の段落頭に立つ条項番号 {len(_xmlseq445)} 件が本文の条項列と順序・個数まで一致",
            (f"Check 445d: 段落分割が本文の条項構造と食い違っている "
             f"(本文 {len(_clauses445)} 件 / XML {len(_xmlseq445)} 件"
             + (f"・重複 {sorted(set(_extra445))[:5]}" if _extra445 else "") + ")。"
             "**折り返しの継続行を新段落と誤認すると 1 つの文が 2 つに割れる** —— 割れた後半が"
             "実在の条項番号で始まると 445b/445c のどちらにも掛からず、445a の regenerate-compare も"
             "生成器が壊れていれば壊れた出力どうしで一致してしまう。"
             "`generate_spdx_license_xml.py` の段落判定を**インデント込み**で行え"),
            blocking=True,
        )

        # 445e — standardLicenseHeader が §16.1 の通知文から導出されている。
        # [ADD 2026-08-23] SPDX ツールはこの要素で **ソースファイルに書かれた通知**を照合する。
        #   §16.2 は「識別子・SPDX タグ・名称による参照で十分な通知になる」と述べているので、
        #   header が欠けると **識別子タグは拾えても散文の通知が拾えない** —— 宣言が届かない。
        #   §16.1 の通知文の実体 (SPDX 識別子行 / 全文への導線 / 名称と版数) が header に
        #   現れることを検証する。可変部 (`<location of this file>`) は `<alt>` で表すのが
        #   SPDX の作法で、§16.4 (本文を改変して同名配布しない) とは衝突しない ——
        #   **header は Work に添える通知であって Dedication の本文ではない** (§16.5)。
        _hdr445 = ""
        try:
            _h = _ET445.fromstring(_xml445.read_text(encoding="utf-8")).find(
                ".//{http://www.spdx.org/license}standardLicenseHeader")
            if _h is not None:
                _hdr445 = " ".join("".join(_e.itertext()) for _e in
                                   _h.findall("{http://www.spdx.org/license}p"))
        except Exception:
            _hdr445 = ""
        # [FIX 2026-08-24] 期待値を **§16.1 から導出**する。従来は 3 つのマーカーを
        #   リテラルで持っており、§16.1 に行を足しても検査対象にならなかった ——
        #   実際、生成器の側もハードコードした接頭辞リストで絞っていたため、追加した
        #   「Machine learning … a patent licence is granted.」が **header から silent に
        #   落ちたのに 445e は緑のまま**だった。通知ブロックは条項本文より深く
        #   インデントされている (条項継続 = 7 / 通知 = 11) ので、そこから導ける。
        _need445e = []
        try:
            _i445 = _src445.index("16.1 To apply this Dedication")
            _blk445 = _src445[_i445:_src445.index("16.2", _i445)]
            _need445e = [_l.strip() for _l in _blk445.splitlines()
                         if _l.strip() and (len(_l) - len(_l.lstrip())) >= 11]
        except ValueError:
            _need445e = []
        # header は 79 桁の折り返しを畳むので、比較も空白を潰した上で部分一致で見る。
        _flat445 = " ".join(_hdr445.split())
        _missh445 = [_n for _n in _need445e
                     if " ".join(_n.split()) not in _flat445
                     and not _n.startswith("Full text:")]   # 可変部は <alt> になる
        _has_alt445 = "<alt " in _xml445.read_text(encoding="utf-8")
        check(
            _hdr445 and _need445e and not _missh445 and _has_alt445,
            f"Check 445e: standardLicenseHeader が §16.1 の通知文 {len(_need445e)} 行を"
            "すべて担っている",
            (f"Check 445e: standardLicenseHeader が欠落/不完全 (欠け: {_missh445}"
             + ("" if _has_alt445 else " / 可変部の <alt> が無い") + ")。"
             "**SPDX ツールはこの要素でソースファイル中の通知を照合する** —— 欠けると "
             "SPDX-License-Identifier タグは拾えても、§16.1 が定める散文の通知は認識されない。"
             "`generate_spdx_license_xml.py` の `_standard_header()` は §16.1 から導出するので、"
             "本文側の通知文を変えたら再生成せよ"),
            blocking=True,
        )

    # ── 451. ACD-1.0 の機械可読記述子が条文と整合すること (BLOCKING) ─────────────────
    # ACD-1.0 §6.5 は「**自動化されたシステムが判定できない許諾は、学習されるための著作物に
    # とっては許諾ではない**」と述べる。そう述べるライセンス自身が機械から判定できないのは
    # 自己矛盾なので、`LICENSES/ACD-1.0.machine.json` を置いている (非 operative・採用者が
    # そのままコピーできる形)。ただし**second source of truth は必ず drift する**ので、
    # 3 面を BLOCKING で縛る:
    #   451a: 記述子が引く clause 番号がすべて本文に実在する (引用先の捏造/番号ずれを防ぐ)
    #   451b: 記述子の notice が §16.1 の通知文と一致する (通知の二重管理を防ぐ)
    #   451c: 公開 manifest の license ブロックと boolean が食い違わない
    #         (`ai_training_permitted` / `tdm_reservation` / `attribution_required`)
    _md451 = ROOT / "LICENSES" / "ACD-1.0.machine.json"
    _lic451 = ROOT / "LICENSES" / "ACD-1.0.txt"
    if _md451.exists() and _lic451.exists():
        import json as _json451
        _src451 = _lic451.read_text(encoding="utf-8")
        _nums451 = set(re.findall(r"^  (\d+\.\d+)\s", _src451, re.M))
        try:
            _d451 = _json451.loads(_md451.read_text(encoding="utf-8"))
        except ValueError as _e451:
            _d451 = None
            check(False, "", f"Check 451: ACD-1.0.machine.json が JSON として不正: {_e451}",
                  blocking=True)
        if _d451 is not None:
            _cited451 = []

            def _walk451(o):
                if isinstance(o, dict):
                    if "clause" in o and isinstance(o["clause"], str):
                        _cited451.append(o["clause"])
                    for _v in o.values():
                        _walk451(_v)
                elif isinstance(o, list):
                    for _v in o:
                        _walk451(_v)

            _walk451(_d451)
            _bad451 = sorted({_c for _c in _cited451 if _c not in _nums451})
            check(
                bool(_cited451) and not _bad451,
                f"Check 451a: 機械可読記述子が引く {len(_cited451)} 件の clause がすべて本文に実在",
                (f"Check 451a: ACD-1.0.machine.json が実在しない条項を引いている: {_bad451}。"
                 "**記述子は条文の要約ではなく索引**なので、番号がずれた時点で「根拠を辿れる」"
                 "という唯一の価値が消える。条項を再採番したら記述子も同一 commit で追従させよ"),
                blocking=True,
            )
            # 451b — notice が §16.1 の通知文と一致する
            _n451 = " ".join((_d451.get("notice") or "").split())
            _blk451 = ""
            try:
                _i451 = _src451.index("16.1 To apply this Dedication")
                _body451 = _src451[_i451:_src451.index("16.2", _i451)]
                _blk451 = " ".join(
                    " ".join(_l.split()) for _l in _body451.splitlines()
                    if _l.strip() and (len(_l) - len(_l.lstrip())) >= 11
                )
            except ValueError:
                _blk451 = ""
            check(
                bool(_n451) and _n451 and _n451 in _blk451,
                "Check 451b: 記述子の notice が §16.1 の通知文と一致",
                (f"Check 451b: 記述子の notice が §16.1 の通知文に含まれない。"
                 f"記述子={_n451[:70]!r} / §16.1={_blk451[:70]!r}。"
                 "通知文を二重管理すると、片方だけ更新した瞬間に**採用者が古い通知を貼る**"),
                blocking=True,
            )
            # 451c — 公開 manifest の license boolean と食い違わない
            _man451 = ROOT / ".well-known" / "aio-manifest.json"
            _pairs451 = [
                ("ai_training_permitted", ("permissions", "machineLearningTraining"), True),
                ("tdm_reservation", ("reservationsAndLimits", "tdmReservation"), False),
                ("attribution_required", ("requirements", "attribution"), False),
            ]
            _mis451 = []
            if _man451.exists():
                try:
                    _lic_blk451 = _json451.loads(_man451.read_text(encoding="utf-8")).get("license", {})
                except ValueError:
                    _lic_blk451 = {}
                for _mk451, _path451, _ in _pairs451:
                    _mv451 = _lic_blk451.get(_mk451)
                    _dv451 = (_d451.get(_path451[0], {}) or {}).get(_path451[1], {}).get("value")
                    if _mv451 is not None and _dv451 is not None and _mv451 != _dv451:
                        _mis451.append(f"{_mk451}: manifest={_mv451} / 記述子={_dv451}")
                # 登録状態 (記述子では top-level の真偽値)。manifest がそれを名乗るなら一致させる
                # (2026-09-24: manifest の license ブロックだけが未登録であることを言っていなかった)
                for _mk451, _dk451 in (("spdx_listed", "spdxListed"), ("osi_approved", "osiApproved")):
                    _mv451 = _lic_blk451.get(_mk451)
                    _dv451 = _d451.get(_dk451)
                    if _mv451 is None:
                        _mis451.append(f"{_mk451}: manifest に無い (記述子={_dv451}) —— 未登録の識別子を"
                                       "spdx_id として名乗る面が、登録状態を言わない")
                    elif _mv451 != _dv451:
                        _mis451.append(f"{_mk451}: manifest={_mv451} / 記述子={_dv451}")
            check(
                not _mis451,
                "Check 451c: 記述子と公開 manifest の license boolean が一致",
                (f"Check 451c: 機械可読な license の主張が面ごとに食い違っている: {_mis451}。"
                 "**判定する側はどちらか一方しか読まない**ので、食い違いは片方の読み手を"
                 "確実に誤らせる (C6 の『全公開面で食い違わない』の license 面)"),
                blocking=True,
            )
    else:
        check(False, "Check 451: ACD-1.0.machine.json と本文が存在",
              "Check 451: LICENSES/ACD-1.0.machine.json もしくは ACD-1.0.txt が無い",
              blocking=True)

    # 451d — 1.0 以外の版の記述子も、その版の本文と照合する (2026-10-17)
    #   `ACD-1.1.machine.json` の `$comment` は「各事実が引く条項が本文に実在することを BLOCKING の
    #   CI 検査が確かめる」と自分で述べていたが、**451a〜c は 1.0 しか見ていなかった** ——
    #   凍結された記述子が、自分を守っていない検査を名指ししていた。1.1 は凍結中で直せないので、
    #   **記述子の側ではなく検査の側を、その主張が真になるように広げる**。版を確定するたびに
    #   記述子が 1 つ増えるので、対象は glob で導出する（決め打ちにすると次の版で黙って外れる）。
    #   照合するのは 451a / 451b と同じ 2 面 + `text` が自分の版の本文を指すこと。
    import json as _json451d
    _bad451d = []
    _seen451d = []
    for _md in sorted((ROOT / "LICENSES").glob("ACD-*.machine.json")):
        _ver = _md.name[len("ACD-"):-len(".machine.json")]
        if _ver == "1.0":
            continue
        _seen451d.append(_ver)
        _txt = ROOT / "LICENSES" / f"ACD-{_ver}.txt"
        if not _txt.exists():
            _bad451d.append(f"{_md.name}: 対応する本文 ACD-{_ver}.txt が無い")
            continue
        _src = _txt.read_text(encoding="utf-8")
        _nums = set(re.findall(r"^  (\d+\.\d+)\s", _src, re.M))
        try:
            _d = _json451d.loads(_md.read_text(encoding="utf-8"))
        except ValueError as _e:
            _bad451d.append(f"{_md.name}: JSON として不正 ({_e})")
            continue
        _cited = []

        def _walk451d(o):
            if isinstance(o, dict):
                if "clause" in o and isinstance(o["clause"], str):
                    _cited.append(o["clause"])
                for _v in o.values():
                    _walk451d(_v)
            elif isinstance(o, list):
                for _v in o:
                    _walk451d(_v)

        _walk451d(_d)
        _miss = sorted({_c for _c in _cited if _c not in _nums})
        if not _cited:
            _bad451d.append(f"{_md.name}: clause を 1 件も引いていない")
        if _miss:
            _bad451d.append(f"{_md.name}: 本文に無い条項を引いている {_miss}")
        _n = " ".join((_d.get("notice") or "").split())
        _blk = ""
        try:
            _i = _src.index("16.1 To apply this Dedication")
            _body = _src[_i:_src.index("16.2", _i)]
            _blk = " ".join(" ".join(_l.split()) for _l in _body.splitlines()
                            if _l.strip() and (len(_l) - len(_l.lstrip())) >= 11)
        except ValueError:
            _blk = ""
        if not _n or _n not in _blk:
            _bad451d.append(f"{_md.name}: notice が ACD-{_ver}.txt の §16.1 に含まれない")
        if not str(_d.get("text", "")).endswith(f"/LICENSES/ACD-{_ver}.txt"):
            _bad451d.append(f"{_md.name}: text が自分の版の本文を指していない ({_d.get('text')!r})")
        if str(_d.get("version", "")) != _ver or str(_d.get("spdxId", "")) != f"ACD-{_ver}":
            _bad451d.append(f"{_md.name}: version/spdxId が file 名の版 {_ver} と一致しない")
    check(
        bool(_seen451d) and not _bad451d,
        f"Check 451d: 1.0 以外の版の記述子 {_seen451d} がそれぞれの本文と整合",
        (f"Check 451d: 版ごとの記述子が本文と食い違う: {_bad451d or '1.0 以外の記述子が 1 つも無い'}。"
         "**記述子は自分の版の条文の索引**であり、凍結された記述子は自分を守る検査を名指ししている"),
        blocking=True,
    )

    # ── 452. 提出準備マーカーが実態と一致すること (BLOCKING) ─────────────────────────
    # `LICENSES/READY-TO-SUBMIT.md` は「レビュー結果を見たいと思える水準に達した」という判断を
    # **ファイルの存在**で表すマーカーで、`ACD-1.0.submission.md` が「これが無い限り送るな」と
    # 参照している。**マーカーは腐ると最も危険な文書**である —— 条文を改訂したあと数値が古い
    # ままだと、読み手は「達した」という判断を **別のテキストについて**読むことになる。
    # 存在するときだけ、主張する実測値 (節数 / 項数 / 行数) と参照ファイルの実在を検証する。
    _rts452 = ROOT / "LICENSES" / "READY-TO-SUBMIT.md"
    _lic452 = ROOT / "LICENSES" / "ACD-1.0.txt"
    if _rts452.exists() and _lic452.exists():
        _src452 = _lic452.read_text(encoding="utf-8")
        _txt452 = _rts452.read_text(encoding="utf-8")
        _real452 = {
            "節": len(re.findall(r"^\d+\. [A-Z]", _src452, re.M)),
            "項": len(re.findall(r"^  \d+\.\d+\s", _src452, re.M)),
            "行": len(_src452.splitlines()),
        }
        _claim452 = re.search(r"(\d+) 節 / (\d+) 項 / (\d+) 行", _txt452)
        _bad452 = []
        if not _claim452:
            _bad452.append("実測値の記載 (`N 節 / N 項 / N 行`) が見つからない")
        else:
            for _k452, _v452 in zip(("節", "項", "行"), _claim452.groups()):
                if int(_v452) != _real452[_k452]:
                    _bad452.append(f"{_k452}: 記載={_v452} / 実測={_real452[_k452]}")
        # 参照先は**文中から導出**する。ハードコードした一覧を「文中に現れたら見る」形にすると、
        # **参照を別の名前へ書き換えた瞬間に検査対象から外れる** (2026-08-24 の非 vacuity 検証で
        # 実測: `ACD-1.0.spdx.xml` を存在しない名前へ替えても緑のままだった)。
        for _ref452 in sorted(set(re.findall(
                r"(?:LICENSES|docs|\.github)/[\w./-]+\.(?:txt|md|xml|json|py)", _txt452))):
            if not (ROOT / _ref452).exists():
                _bad452.append(f"参照先が無い: {_ref452}")
        check(
            not _bad452,
            f"Check 452: 提出準備マーカーが実態と一致 ({_real452['節']} 節 / "
            f"{_real452['項']} 項 / {_real452['行']} 行)",
            (f"Check 452: READY-TO-SUBMIT.md が実態とずれている: {_bad452}。"
             "**マーカーは腐ると最も危険な文書** —— 条文を改訂したあと数値が古いままだと、"
             "読み手は「レビュー結果を見たい水準に達した」という判断を **別のテキストについて** "
             "読むことになる。条文を触ったら同一 commit で数値も更新せよ "
             "(判断そのものを撤回するなら、ファイルを削除するのが正しい)"),
            blocking=True,
        )

    # ── 453. 凍結中のライセンス提出物が動かないこと (BLOCKING) ───────────────────────
    # 2026-08-24、オーナーが SPDX / OSI へ申請するため「結果を伝えるまでライセンスをそのままに
    # しておいてほしい」と述べた。**「触らない」を記憶や善意に委ねない。** このリポジトリは AI が
    # 無限に自走して改善を続ける前提で動いており、**次のセッションの担当はその会話を見ていない**。
    # 凍結を git 上の成果物 (`LICENSES/FROZEN.md`) にして BLOCKING で縛れば、うっかり触った時点で
    # CI が赤くなって止まる。存在するときだけ有効 (解除は FROZEN.md の削除で表す)。
    #
    # **回避の抑止**: sha256 を書き換えれば Check は黙るので、期待値の変更そのものを疑わしい
    # 操作として扱う —— 表の行数と対象 path の集合も pin し、行を減らす/対象を差し替える形の
    # 「実質的な解除」を検出する。本文に欠陥を見つけたときの正しい行動は、直すことではなく
    # **オーナーへ報告すること**である (審査中の差し替えは、審査側が見ているテキストとの乖離を生む)。
    _fz453 = ROOT / "LICENSES" / "FROZEN.md"
    if _fz453.exists():
        import hashlib as _hl453
        _txt453 = _fz453.read_text(encoding="utf-8")
        _rows453 = re.findall(r"^([0-9a-f]{64})  (\S+)$", _txt453, re.M)
        # **必須の下限**。ここから*外す*ことは実質的な凍結解除なので禁じる。
        # **足すことは禁じない** —— 版が確定するたびに凍結対象は増える
        # (`REVISION-PROTOCOL.md` §2「1.0 は永久凍結・次版は併置」)。
        # **2026-09-17 に 1.1 を確定させたときに、集合の完全一致がその正当な追加を止めた** ——
        # 集合を凍結していたのは「外させない」ためであって「増やさせない」ためではない。
        # ただし**何でも足せる**ようにはしない: 追加は `LICENSES/ACD-<版>.…` の形に限る
        # (無関係な file を凍結対象へ紛れ込ませると、その file が触れなくなる)。
        _EXPECT453 = {
            "LICENSES/ACD-1.0.txt",
            "LICENSES/ACD-1.0.spdx.xml",
            "LICENSES/ACD-1.0.machine.json",
        }
        _bad453 = []
        _paths453 = {_p for _, _p in _rows453}
        _missing453 = sorted(_EXPECT453 - _paths453)
        if _missing453:
            _bad453.append(
                f"凍結対象が FREEZE-DATA から外されている: {_missing453}。"
                "**対象を外すのは実質的な凍結解除**であり、解除は FROZEN.md の削除で表す"
            )
        _shape453 = re.compile(r"^LICENSES/ACD-\d+\.\d+\.[A-Za-z.]+$")
        _odd453 = sorted(_p for _p in _paths453 - _EXPECT453 if not _shape453.match(_p))
        if _odd453:
            _bad453.append(
                f"凍結対象に版の成果物でない path が入っている: {_odd453}。"
                "**凍結は版のテキストと、その版に付随する機械可読成果物についての約束**である"
            )
        for _h453, _rel453 in _rows453:
            _f453 = ROOT / _rel453
            if not _f453.exists():
                _bad453.append(f"凍結対象が存在しない: {_rel453}")
                continue
            _actual453 = _hl453.sha256(_f453.read_bytes()).hexdigest()
            if _actual453 != _h453:
                _bad453.append(
                    f"{_rel453} が凍結後に変更されている "
                    f"(記録={_h453[:12]}… / 実測={_actual453[:12]}…)"
                )
        check(
            bool(_rows453) and not _bad453,
            f"Check 453: 凍結中のライセンス提出物 {len(_rows453)} 件が申請時点のまま",
            (f"Check 453: 凍結が破られている: {_bad453}。"
             "オーナーが SPDX / OSI へ申請中で、**結果を伝えるまでテキストを動かさない**という"
             "依頼のもとにある (LICENSES/FROZEN.md)。**sha256 を書き換えて Check を黙らせるのは"
             "凍結の趣旨に反する** —— 本文に是正すべき欠陥を見つけた場合でも、直すのではなく"
             "オーナーへ報告せよ。審査中の差し替えは、審査側が見ているテキストとの乖離を生む。"
             "解除はオーナーが結果を伝えたときに FROZEN.md を削除して行う"),
            blocking=True,
        )
