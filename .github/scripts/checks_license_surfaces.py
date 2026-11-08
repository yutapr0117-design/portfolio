"""
checks_license_surfaces.py — ライセンスの提出物と凍結の Check 群 (445 / 451 / 452 / 453 / 490)
(2026-10-26 に checks_aio_config.py から切り出した — 980 行で Check 52 の advisory 950 を超え、
1,000 行の BLOCKING (Check 365) まで 20 行だった。OSI の作業で最も触る検査なので、止まる前に分けた)。

(444 ライセンス宣言の cross-surface coherence は 2026-11-08 に checks_license_declaration.py へ分けた —
938 行で Check 52 の advisory 900 を超えた。) 445 SPDX 提出用 XML の同期 / 451 機械可読記述子と条文 /
452 提出準備マーカー / 453 凍結中の提出物。いずれも自前で対象 file を読み、checks_aio_config.py の
他の Check (62-69) と変数を共有しない。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
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
       451e: 1.3 より後の版の記述子は、gap を担う §6 / §8 / §9 をすべて引くこと (2026-11-01)。
       451f: 記述子の散文 (note など) が引く section と引用が、その版の本文に在ること (2026-11-08)。
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
       本文に欠陥を見つけたときの正しい行動は、凍結した本文を直すことではなく、errata に
       記録して次版の草案で直すこと (審査中の差し替えは、審査側が見ているテキストとの乖離を
       生む。2026-11-02 訂正: 旧文は「オーナーへ報告すること」)。 (BLOCKING)
       453b: 冒頭で FROZEN TEXT を名乗る版の本文と、あればその記述子・SPDX XML が FREEZE-DATA に pin されていること (2026-11-01)。
  490. 確定した本文が、確定の作業で壊れていないこと (BLOCKING・2026-11-06)。Check 468 は草案しか見ず、
       Check 453 は pin した byte しか見ないので、草案から確定本文を作る手作業の誤りを見る層が無かった。
       490a 1 行目が file 名の版を FROZEN TEXT と名乗る / 490b 題名の版が file 名と一致 / 490c 節が
       直前の版と同じ数だけ連番でそろい END OF TERMS で終わる / 490d 冒頭の語数・条数の申告が直前の版と
       この版の実測に一致 / 490e 冒頭が名指す CHANGELIST がこの版のもので、実在する。
       490f 申請する版 (SUBMISSION-TARGET) の冒頭が提出状況を現在形で述べない (申請した瞬間に偽になり、
       凍結中なので直せない。日付つきの過去形にする・1.1〜1.3 は申請しない版なので現在形のままで正しい)。
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

    # ── 445. SPDX 提出用 XML がライセンス本文と同期していること (BLOCKING) ─────────────
    # 提出物を手書きすると本文の改善に追従せず silent に古くなる。単一ソース (ACD-1.0.txt) から
    # 導出し、ここで「再生成して一致するか」を検証する (Check 121 と同じ regenerate-compare)。
    import subprocess as _sp445
    import xml.etree.ElementTree as _ET445
    _xml445 = ROOT / "LICENSES" / "ACD-1.0.spdx.xml"
    # **全版の XML を照合する (2026-11-01)**: 生成器は `--version` で任意の版の XML を作れるようになった。
    # 出す版の XML を置いた日から、その版も同じ 445a〜e で守る (決め打ちだと、置いた XML が無検査になる)。
    # 1.0 の XML は凍結された提出物 (Check 453) なので、存在必須は 1.0 だけ。
    _xmls445 = sorted((ROOT / "LICENSES").glob("ACD-*.spdx.xml"))
    _gen445 = ROOT / ".github" / "scripts" / "generate_spdx_license_xml.py"
    if not (_xml445.exists() and _gen445.exists()):
        check(False, "", f"Check 445: SPDX 提出物または生成器が無い "
                         f"(xml={_xml445.exists()} / generator={_gen445.exists()})", blocking=True)
    else:
        for _xml445 in _xmls445:
            _ver445 = _xml445.name[len("ACD-"):-len(".spdx.xml")]
            # 445a — 再生成して一致するか
            _r445 = _sp445.run([sys.executable, str(_gen445), "--check", "--version", _ver445],
                               cwd=str(ROOT), capture_output=True, text=True)
            check(
                _r445.returncode == 0,
                f"Check 445a: SPDX 提出用 XML (ACD-{_ver445}) が本文と同期している",
                (f"Check 445a: SPDX 提出用 XML が本文と同期していない — `npm run spdx-xml` を実行して "
                 f"commit せよ。**提出物は手で編集しない** (単一ソースは LICENSES/ACD-{_ver445}.txt)。"
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
            _src445 = (ROOT / "LICENSES" / f"ACD-{_ver445}.txt").read_text(encoding="utf-8")
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
                _blk445 = _src445[_i445:_src445.index("\n  16.2 ", _i445)]
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
                _body451 = _src451[_i451:_src451.index("\n  16.2 ", _i451)]
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
                    # 欠けた答えも不一致として数える (2026-11-08: 鍵の改名・削除・null で答えが manifest から
                    #   消えても OK のままだった。同じ節の spdx_listed / osi_approved と揃えた)
                    if _mv451 is None or _dv451 is None or _mv451 != _dv451:
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
    _tgt451e = []
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
            # 行頭で探す: 1.4 の §16.1 は本文で "Section 16.2" を引くので、素の "16.2" だと通知文の手前で切れる
            #   (2026-11-06 の段 7 で判明。確定の日に正しい記述子が 451d で赤くなるところだった)。
            _body = _src[_i:_src.index("\n  16.2 ", _i)]
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
        # 451e (2026-11-01・portfolio-bb の提案 / against.md #269(b)): PREAMBLE が名乗る gap は
        #   機械学習・特許・機械生成の 3 つで、条文では §6 / §8 / §9 が担う (468d と同じ対応)。
        #   1.1〜1.3 の記述子は §9 を指すキーを 1 つも持たず、**記述子だけを読む消費者には 3 つ目の
        #   gap が存在しない**。凍結で直せないので、1.3 より後の版の記述子から要求する
        #   (記述子は版の確定で作られるので、次の確定の日に効く)。
        try:
            _vt451e = tuple(int(_x) for _x in _ver.split("."))
        except ValueError:
            _vt451e = (0,)
        if _vt451e > (1, 3):
            _tgt451e.append(_ver)
            _secs451e = {_c.split(".", 1)[0] for _c in _cited}
            _lack451e = sorted({"6", "8", "9"} - _secs451e, key=int)
            if _lack451e:
                _bad451d.append(f"451e: {_md.name} が gap を担う §{'/§'.join(_lack451e)} を 1 つも引いていない "
                                "(PREAMBLE の 3 つの gap が記述子から見えない)")
        # 451f (2026-11-08・portfolio-aa の問い): 451a〜e は `clause` と notice と boolean しか見ず、note などの
        #   散文を読んでいなかった。散文が引く section の番号と "…" の引用は、自分の版の本文に在ること。
        #   散文が本文より広い約束を述べていないかは機械に見えないので、確定の日に人が読む。
        _norm451f = " ".join(_src.split())
        _secs451f = {_c.split(".", 1)[0] for _c in _nums}
        _strs451f = []

        def _walk451f(o, k=""):
            if isinstance(o, dict):
                for _k, _v in o.items():
                    _walk451f(_v, _k)
            elif isinstance(o, list):
                for _v in o:
                    _walk451f(_v, k)
            elif isinstance(o, str) and k not in ("$comment", "notice", "clause", "text"):
                _strs451f.append(o)

        _walk451f(_d)
        for _s in _strs451f:
            for _r in re.finditer(r"\b[Ss]ections?\s+(\d+(?:\.\d+)?(?:(?:,\s*|\s+and\s+|\s+or\s+|\s+to\s+)\d+(?:\.\d+)?)*)", _s):
                for _c in re.findall(r"\d+(?:\.\d+)?", _r.group(1)):
                    if _c not in (_nums if "." in _c else _secs451f):
                        _bad451d.append(f"451f: {_md.name} の散文が ACD-{_ver}.txt に無い section {_c} を引く")
            for _q in re.findall(r'"([^"]{6,})"', _s):
                if " ".join(_q.split()) not in _norm451f:
                    _bad451d.append(f"451f: {_md.name} の散文の引用 {_q[:40]!r} が ACD-{_ver}.txt に無い")
    check(
        bool(_seen451d) and not _bad451d,
        (f"Check 451d: 1.0 以外の版の記述子 {_seen451d} がそれぞれの本文と整合 "
         f"(451e の対象 = 1.3 より後の記述子: {_tgt451e or 'まだ無い —— 版の確定時に作られ、その日から効く'})"),
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
    else:
        # 対象が無いのに黙って skip しない (2026-11-02): 改名・移動を正しく済ませると他の Check は全部緑のまま、
        # ここだけが OK も ERROR も出さずに消える (460 / 469 で踏んだ形)。
        check(False, "Check 452: 対象ファイル",
              f"Check 452: 検査対象 {_rts452.relative_to(ROOT).as_posix()} / {_lic452.relative_to(ROOT).as_posix()} が無い —— 改名・移動したならこの Check の参照先を直す (黙って skip しない)")

    # ── 453. 凍結中のライセンス提出物が動かないこと (BLOCKING) ───────────────────────
    # 2026-08-24、オーナーが SPDX / OSI へ申請するため「結果を伝えるまでライセンスをそのままに
    # しておいてほしい」と述べた。**「触らない」を記憶や善意に委ねない。** このリポジトリは AI が
    # 無限に自走して改善を続ける前提で動いており、**次のセッションの担当はその会話を見ていない**。
    # 凍結を git 上の成果物 (`LICENSES/FROZEN.md`) にして BLOCKING で縛れば、うっかり触った時点で
    # CI が赤くなって止まる。存在するときだけ有効 (解除は FROZEN.md の削除で表す)。
    #
    # **回避の抑止**: sha256 を書き換えれば Check は黙るので、期待値の変更そのものを疑わしい
    # 操作として扱う —— 表の行数と対象 path の集合も pin し、行を減らす/対象を差し替える形の
    # 「実質的な解除」を検出する。本文に欠陥を見つけたときの正しい行動は、凍結した本文を直す
    # ことではなく、errata に記録して次版の草案で直すことである (審査中の差し替えは、審査側が
    # 見ているテキストとの乖離を生む。2026-11-02 訂正: 旧文は「オーナーへ報告すること」)。
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
             "凍結の趣旨に反する** —— 本文に是正すべき欠陥を見つけた場合でも、凍結した本文は"
             "直さず、LICENSES/ACD-1.0.errata.md に記録して次版の草案で直せ。審査中の差し替えは、"
             "審査側が見ているテキストとの乖離を生む。"
             "解除はオーナーが結果を伝えたときに FROZEN.md を削除して行う"),
            blocking=True,
        )
        # 453b — 自分で「FROZEN TEXT」と名乗る版の本文 (と、あればその記述子) が FREEZE-DATA に入っていること。
        #   2026-11-01 の版移行シミュレーション (172 観点の I18) で、1.4 を確定して冒頭に FROZEN TEXT と
        #   書いた `ACD-1.4.txt` を **FREEZE-DATA に足し忘れても何も鳴らない**ことを実測した —— 453 は
        #   列挙された file しか見ないので、凍結を名乗る本文が**黙って編集可能なまま**残る。審査者が依拠する
        #   「stable text」の約束がそこで切れる。宣言 (本文の冒頭) から導出して pin の有無を照合する。
        _unpinned453b = []
        for _t453b in sorted((ROOT / "LICENSES").glob("ACD-*.txt")):
            if _t453b.name.endswith("-DRAFT.txt"):
                continue
            if "FROZEN TEXT" not in _t453b.read_text(encoding="utf-8").split("\n", 1)[0]:
                continue
            _rel453b = f"LICENSES/{_t453b.name}"
            if _rel453b not in _paths453:
                _unpinned453b.append(_rel453b)
            # 付随する成果物 (記述子・SPDX XML) も同じ版の提出物なので、置いたなら pin する
            # (1.0 は 3 点とも pin 済み。SPDX XML は `generate_spdx_license_xml.py --version` で
            # 後の版にも作れるようになった・2026-11-01)。
            for _suf453b in (".machine.json", ".spdx.xml"):
                _art453b = _t453b.with_name(_t453b.name[:-len(".txt")] + _suf453b)
                if _art453b.exists() and f"LICENSES/{_art453b.name}" not in _paths453:
                    _unpinned453b.append(f"LICENSES/{_art453b.name}")
        check(
            not _unpinned453b,
            "Check 453b: 冒頭で FROZEN TEXT を名乗る版の本文と、置いてある記述子・SPDX XML はすべて FREEZE-DATA に入っている",
            (f"Check 453b: 凍結を名乗るのに sha256 が pin されていない: {_unpinned453b}。"
             "**版を確定したら、その本文 (と記述子・SPDX XML) を FROZEN.md の FREEZE-DATA に足す** —— 足さないと"
             "凍結を名乗る本文が黙って編集可能なまま残り、審査者が依拠する stable text の約束が切れる"),
            blocking=True,
        )

    # ── 490. 確定した本文が、確定の作業で壊れていないこと (BLOCKING) ──────────────────
    # 版の確定は、草案の冒頭を差し替えて本文を別の file へ移す手作業である。Check 468 は草案しか見ず、
    # Check 453 は pin した byte しか見ないので、この手作業の誤りはどの層にも見えなかった。2026-11-06 に
    # 使い捨ての worktree で 1.4 を確定し、誤りを 8 種入れて測ると 7 種が無音だった (最後の節が欠けても、
    # 題名が前の版のままでも緑)。凍結すると直せないので、pin する前に落とす。
    _sep490 = "-" * 80
    _vers490 = []
    for _p490 in (ROOT / "LICENSES").glob("ACD-*.txt"):
        _m490 = re.match(r"ACD-(\d+)\.(\d+)\.txt$", _p490.name)
        if _m490:
            _vers490.append(((int(_m490.group(1)), int(_m490.group(2))), _p490.read_text(encoding="utf-8")))
    _vers490.sort(key=lambda _x: _x[0])

    def _size490(_t):
        _b = _t.split(_sep490, 1)[1] if _sep490 in _t else _t
        return len(_b.split()), len(set(re.findall(r"^  (\d+\.\d+) ", _b, re.M)))

    _sub490 = ROOT / "LICENSES" / "ACD-1.0.submission.md"
    _tm490 = re.search(r"<!-- SUBMISSION-TARGET: (ACD-\d+\.\d+) -->", _sub490.read_text(encoding="utf-8") if _sub490.exists() else "")
    _target490 = _tm490.group(1) if _tm490 else None
    _bad490 = [] if _target490 else ["490f: ACD-1.0.submission.md に SUBMISSION-TARGET marker が無い"]
    for _i490, (_v490, _t490) in enumerate(_vers490):
        if _i490 == 0:
            continue  # 最初の版 (1.0) は冒頭を持たず、本文そのものである
        _vs490 = f"{_v490[0]}.{_v490[1]}"
        _pv490, _pt490 = _vers490[_i490 - 1]
        _ps490 = f"{_pv490[0]}.{_pv490[1]}"
        _first490 = _t490.split("\n", 1)[0]
        if not _first490.startswith(f"ACD-{_vs490} -- FROZEN TEXT.") or "DRAFT" in _first490 or "NOT IN FORCE" in _first490:
            _bad490.append(f"490a: ACD-{_vs490}.txt の 1 行目が自分を確定本文と名乗らない: {_first490[:70]!r}")
        _head490, _, _body490 = _t490.partition(_sep490)
        _title490 = re.search(r"^\s+Version (\d+\.\d+)\s*$", _body490, re.M)
        if not _title490 or _title490.group(1) != _vs490:
            _bad490.append(f"490b: ACD-{_vs490}.txt の題名の版が違う: {_title490.group(1) if _title490 else '無い'}")
        _secs490 = [int(_x) for _x in re.findall(r"^(\d+)\. [A-Z]", _body490, re.M)]
        _psecs490 = len(re.findall(r"^\d+\. [A-Z]", _pt490.partition(_sep490)[2] or _pt490, re.M))
        if _secs490 != list(range(1, _psecs490 + 1)) or not _body490.rstrip().endswith("END OF TERMS"):
            _bad490.append(f"490c: ACD-{_vs490}.txt の本文が欠けている (節 {_secs490[-1:] or '無し'} / 直前の版 {_psecs490} 節 / 末尾 END OF TERMS)")
        _h490 = " ".join(_head490.split())
        _r490 = re.search(r"ACD-(\d+\.\d+): ([\d,]+) words, (\d+) clauses\. This version: ([\d,]+) words, (\d+) clauses\.", _h490)
        if not _r490:
            _bad490.append(f"490d: ACD-{_vs490}.txt の冒頭に語数と条数の申告が無い")
        else:
            _said490 = (_r490.group(1), int(_r490.group(2).replace(",", "")), int(_r490.group(3)),
                        int(_r490.group(4).replace(",", "")), int(_r490.group(5)))
            _real490 = (_ps490, *_size490(_pt490), *_size490(_t490))
            if _said490 != _real490:
                _bad490.append(f"490d: ACD-{_vs490}.txt の冒頭の申告 {_said490} が実測 {_real490} と違う")
        _cl490 = f"LICENSES/ACD-{_vs490}-CHANGELIST.md"
        if _cl490 not in _h490 or not (ROOT / _cl490).exists():
            _bad490.append(f"490e: ACD-{_vs490}.txt の冒頭が {_cl490} を指していないか、その file が無い")
        if f"ACD-{_vs490}" == _target490 and re.search(r"NOT SUBMITTED|has not been submitted", _head490.replace("\n", " ")):
            _bad490.append(f"490f: 申請する版 ACD-{_vs490} の冒頭が提出状況を現在形で述べる (申請した瞬間に偽になり、凍結中なので直せない)")
    check(
        len(_vers490) >= 2 and not _bad490,
        f"Check 490: 確定した本文 {len(_vers490) - 1} 版の 1 行目・題名・節・語数と条数の申告・CHANGELIST の指し先が実物と合う",
        (f"Check 490: 確定した本文が確定の作業で壊れている: {_bad490 or '版が 2 つ以上見つからない'}。"
         "**凍結して申請すると直せない** —— pin する前に草案から作り直せ"),
        blocking=True,
    )
