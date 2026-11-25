"""
checks_license_entry.py — 審査者が最初に開く入口の面 (入口・送る材料・添付の欄) が、原文と提出対象に合うかを見る Check 群
(extracted from checks_license_references.py — check.py split track・category "entry faces")。

**なぜ切り出したか (2026-11-26・df)**: checks_license_references.py が advisory (600) を越えた (678 行)。残る側は「参照は解決する」
の 1 つの invariant (471・492〜496) を持ち、ここは Check 472 の下位部 (472l〜472p) —— 入口の面の引用・語数・送る本文の版・
添付の欄 —— だけを持つ。472 の本体は checks_license_submission.py に在り、900 行に近いので下位部をこちらへ置いていた。
本文は無改変で移した (行の中身は byte で同じ・字下げも同じ)。

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (472 の下位部だけなので、番号の inventory は
checks_license_submission.py の 472 の項が持つ)
"""
import re
import subprocess


def run(ctx):
    """Run the entry-face sub-checks of 472. ctx carries shared check()/ROOT by reference."""
    ROOT = ctx.ROOT
    check = ctx.check
    # 472l — OSI の FAQ として引く文が rounds/ の本文に在ること (2026-11-06)。Check 472 の下位部だが、
    #   checks_license_submission.py が 900 行に近いのでここに置く。REVIEWERS は FAQ の行の引用を全部、
    #   材料表は "FAQ" の直後の引用だけを見る (同じ長い行に別の出典の引用が並ぶので、行の単位では誤検出する)。
    def _n472l(_t):
        return " ".join(_t.replace("’", "'").replace("“", '"').replace("”", '"').split()).lower()

    _snap472l = sorted((ROOT / "LICENSES" / "rounds").glob("*-osi-faq-*-snapshot.txt"))
    _src472l = _n472l(_snap472l[-1].read_text(encoding="utf-8")) if _snap472l else ""
    _quotes472l = []
    for _f472l in sorted((ROOT / "LICENSES").glob("REVIEWERS*.md")):  # 入口と、入口から移した記録の頁 (2026-11-24・議題 14)
        for _l472l in _f472l.read_text(encoding="utf-8").splitlines():
            if _l472l.startswith("|") and "FAQ" in _l472l:
                from verify_dossier_quotations import italic_quotes as _iq472l  # 内側の引用符を含む引用も拾う
                _quotes472l += [(_f472l.name, _q) for _q in _iq472l(_l472l, 10)]
    _mt472l = (ROOT / "LICENSES" / "SUBMISSION-MATERIALS.md").read_text(encoding="utf-8")
    _quotes472l += [("SUBMISSION-MATERIALS.md", _q) for _q in re.findall(r'(?<!OSAID の )FAQ[^*"]{0,60}\*"([^"]{10,})"\*', _mt472l)]
    _miss472l = [f"{_f}: {_q[:60]}" for _f, _q in _quotes472l if _n472l(_q).rstrip(".,") not in _src472l]
    check(
        len(_quotes472l) >= 8 and not _miss472l,
        f"Check 472l: OSI の FAQ として引く {len(_quotes472l)} 件が rounds/ の本文に在る",
        (f"Check 472l: OSI の FAQ として引く文が保存した本文と違う: {_miss472l or '引用か本文が見つからない'}。"
         "承認されるべき理由の先頭に置いた出典なので、語を動かさない。REVIEWERS.md の表は「FAQ」の語を含む行の"
         "引用をすべて FAQ の写しに当てるので、FAQ 以外の出典の引用を足すなら行を分けよ"),
        blocking=True,
    )

    # 472m — 入口の短い経路の表の語数が実物と合うこと (2026-11-07・portfolio-00 の依頼)。審査者に示す読む費用で、
    #   objection-map を直すたびに手で書き直していた (同じ日に 2,451 → 2,608)。合計は「≈」なので 10 語の幅を持つ。
    _rv472m = (ROOT / "LICENSES" / "REVIEWERS.md").read_text(encoding="utf-8")
    _map472m = re.search(r"\(ACD-1\.0\.objection-map\.md\) \| \*\*([\d,]+)\*\* \|", _rv472m)
    _lic472m = re.search(r"\(ACD-\d+\.\d+\.txt\) \| \*\*([\d,]+)\*\* \| the licence\b", _rv472m)
    _two472m = re.search(r"\| ~(\d+) \|", _rv472m)
    _sum472m = re.search(r"\*\*≈ ([\d,]+) words\*\*", _rv472m)
    _real472m = len((ROOT / "LICENSES" / "ACD-1.0.objection-map.md").read_text(encoding="utf-8").split())
    _bad472m = []
    if not (_map472m and _lic472m and _two472m and _sum472m):
        _bad472m.append("表の行か合計が読めない")
    else:
        _got472m = [int(_m.group(1).replace(",", "")) for _m in (_lic472m, _two472m, _map472m, _sum472m)]
        if _got472m[2] != _real472m:
            _bad472m.append(f"objection-map {_got472m[2]} 語 / 実測 {_real472m} 語")
        if abs(sum(_got472m[:3]) - _got472m[3]) > 10:
            _bad472m.append(f"合計 ≈ {_got472m[3]} 語 / 3 行の和 {sum(_got472m[:3])} 語")
    # ドシエ全体の語数は増え続けるので 10% の幅を持つ。09-28 の値のまま 3 分の 1 少なく述べていた (2026-11-07)。
    #   閾値は三段で、違うのは意図どおり (2026-11-24・cd の問い): sync_stated_counts.py --apply が差 5% を越えたら先に書き換え、
    #   472m は 8% で ADVISORY、10% で BLOCKING —— sync を回し忘れた PR だけを止める。5% と 10% の間で緑のまま書き換わるのは正常
    _all472m = re.search(r"is \*\*([\d,]+) words\*\*, \*\*(\d+) times the licence\*\*", _rv472m)
    _ls472m = subprocess.run(["git", "ls-files", "-z", "LICENSES", ":!LICENSES/rounds"], cwd=ROOT, text=True, capture_output=True).stdout
    _size472m = sum(len((ROOT / _f).read_text(encoding="utf-8", errors="replace").split()) for _f in _ls472m.split("\0") if _f)
    _dev472m = None
    if not _all472m or not _lic472m:
        _bad472m.append("ドシエ全体の語数の文が読めない")
    else:
        _said472m = int(_all472m.group(1).replace(",", ""))
        _lw472m = int(_lic472m.group(1).replace(",", ""))
        _dev472m = abs(_said472m - _size472m) / _size472m
        if abs(_said472m - _size472m) > _size472m * 0.1:
            _bad472m.append(f"ドシエ全体 {_said472m} 語 / 実測 {_size472m} 語")
        if abs(int(_all472m.group(2)) - _said472m / _lw472m) > 1:
            _bad472m.append(f"{_all472m.group(2)} 倍 / {_said472m} ÷ {_lw472m}")
    check(
        not _bad472m,
        f"Check 472m: 入口の短い経路の表が objection-map の {_real472m} 語と合計に合い、ドシエ全体の語数も 10% の幅に収まる",
        (f"Check 472m: 入口の短い経路の表が実物と違う: {_bad472m}。審査者に示す読む費用なので、"
         "objection-map を直したら同じ commit で表と合計を直せ"),
        blocking=True,
    )
    # 幅の手前で先に鳴らす (2026-11-12・portfolio-aa の提案): 3 人の増分で語数は 1 日に数 % 動き、10% を越えた PR が
    #   他人の増分の分まで直す羽目になる (2973 で起きた)。8% を越えたら、まだ緑のうちに REVIEWERS の数を測り直す合図を出す
    if _dev472m is not None:
        check(_dev472m <= 0.08,
              f"Check 472m (ADVISORY): ドシエ全体の語数の記載と実測の差 {_dev472m:.1%} (8% の手前)",
              f"Check 472m (ADVISORY): ドシエ全体の語数の記載 {_said472m:,} 語と実測 {_size472m:,} 語の差が {_dev472m:.1%} で、"
              "BLOCKING の 10% に近い。次の増分で越える前に REVIEWERS.md の数 (と倍率) を測り直す",
              blocking=False)

    # 472n — 入口の面の斜体の引用が、rounds/ か manifest で解決すること (2026-11-07)。引用を読みやすく動かす誤りが
    #   6 回出て、どれも手の照合でしか見つからなかった。全 corpus は CI に無いので、手元で確かめた引用の hash を置く。
    #   語を 1 つ動かすと hash が外れて RED になる。直し方は --record-entry で原文に当て直すこと。
    import verify_dossier_quotations as _vdq472n
    _entry472n = _vdq472n.entry_quotes(str(ROOT))
    _keys472n, _own472n = _vdq472n.read_entry_manifest(str(ROOT))
    _base472n = _vdq472n.load_sources(str(ROOT), cache=False)
    _miss472n = [f"{_loc}: {_q[:70]}" for _q, _loc in _entry472n.items()
                 if _vdq472n.entry_key(_q) not in _keys472n and _vdq472n.norm(_q) not in _own472n
                 and not _vdq472n.present(_q, _base472n)]
    check(
        len(_entry472n) >= 100 and not _miss472n,
        f"Check 472n: 入口の面の斜体の引用 {len(_entry472n)} 件が rounds/ か確認済みの hash で解決する",
        (f"Check 472n: 入口の面の引用が原文で確かめられていない: {_miss472n or '引用を読めない'}。"
         "`DOSSIER_ARCHIVE_CACHE=<cache> python3 .github/scripts/verify_dossier_quotations.py --record-entry` で原文に当てよ。"
         "我々自身の文なら entry_quotes_verified.txt に own: の行を足す"),
        blocking=True,
    )

    # 472o — 送る本文が述べる ACD の版が、提出対象であること (2026-11-07)。472f は欄の 16 箇所しか見ず、切り替えた日に
    #   "I affirm that ACD-1.0 complies" のように本文が別の版の適合を宣言したまま送られるところだった。
    _sub472o = (ROOT / "LICENSES" / "ACD-1.0.submission.md").read_text(encoding="utf-8")
    _sub472o = re.sub(r"<!--\s*SUPERSEDED-LETTER:[^>]*-->.*?<!--\s*/SUPERSEDED-LETTER\s*-->", " ", _sub472o, flags=re.S)
    _tg472o = re.search(r"<!--\s*SUBMISSION-TARGET:\s*(ACD-\d+\.\d+)\s*-->", _sub472o)
    # 2026-11-23 (議題 3b の C′): §B.0 は送る手紙から、オーナーが自分の言葉で書くための材料 (事実の箇条と表) になった。材料の
    #   中の版の名は提出対象であること。別の版の名は、出来事の文脈 (posted・sent・drafted・→ の差・record・history) の文だけに
    #   在ってよい。file 名 (ACD-1.0.gap-measurements.md など) は版の主張ではないので数えない
    _start472o = _sub472o.find("### B.0 Facts for the owner's message")
    _end472o = _sub472o.find("### B.1 ", _start472o + 1) if _start472o >= 0 else -1
    _b472o = _sub472o[_start472o:_end472o] if 0 <= _start472o < _end472o else ""
    _ids472o, _bad472o = [], set()
    for _mo in re.finditer(r"(?<![\w-])(ACD-\d+\.\d+)(?!\.[A-Za-z])", _b472o):
        _ids472o.append(_mo.group(1))
        _sent = _b472o[max(_b472o.rfind(". ", 0, _mo.start()), _b472o.rfind("\n", 0, _mo.start()), 0):
                       min(_x for _x in (_b472o.find(". ", _mo.end()), _b472o.find("\n", _mo.end()), len(_b472o)) if _x >= 0)]
        if _tg472o and _mo.group(1) != _tg472o.group(1) and not re.search(r"post(?:ed|ing)|sent|drafted|→|record|history|was rejected", _sent):
            _bad472o.add(_mo.group(1))
    _sup472o = True  # 材料の形では提出対象の名が 3 つ以上在れば足りる
    _bad472o = sorted(_bad472o)
    check(
        sum(1 for _i in _ids472o if _tg472o and _i == _tg472o.group(1)) >= 3 and not _bad472o,
        f"Check 472o: 送る本文が述べる ACD の版 {len(_ids472o)} 箇所が提出対象に合う",
        (f"Check 472o: 送る本文が提出対象でない版を述べている: {_bad472o or '本文か提出対象を読めない'}。"
         "別の版の適合を宣言したまま送らないよう、1 文ずつ読んで提出対象へ向ける"),
        blocking=True,
    )

    # 472p — 添付する本文の欄 (submission.md §A の "Canonical text") の行数・語数・SHA-256 が、欄に書いた再現のコマンドを当てた
    #   出力と一致し、出力が空でないこと (2026-11-23・議題 4・5/0/0・fc)。添付は提出対象の凍結本文の区切り線 (- × 80) より下。
    #   d7 の注意: 題の行に当たらない sed は 0 行を出し、shasum は空の値 (e3b0c442…) を返すので、「一致」だけを見ると空の値で緑に
    #   なる。行数と語数 (length_sites の「題名から」と同じ数え方) も照らし、空なら RED にする
    import hashlib as _h472p
    _sub472p = (ROOT / "LICENSES" / "ACD-1.0.submission.md").read_text(encoding="utf-8")
    _row472p = next((_l for _l in _sub472p.splitlines() if _l.startswith("| Canonical text |")), "")
    _tg472p = re.search(r"<!--\s*SUBMISSION-TARGET:\s*(ACD-\d+\.\d+)\s*-->", _sub472p)
    _bad472p = []
    _vals472p = re.search(r"\(([\d,]+) lines, ([\d,]+) words, SHA-256 `([0-9a-f]{64})`\)", _row472p)
    # 再現のコマンドは shasum -a 256 (mac) と sha256sum (Linux) のどちらの形も読む。欄に両方を併記すれば両方を照らす
    #   (2026-11-24・d7 の候補・6d の依頼: Linux の審査者は sha256sum を使うことが多い)
    _cmds472p = list(re.finditer(r"`sed '1,/\^-\\\{80\\\}\$/d' LICENSES/(ACD-\d+\.\d+)\.txt \\\| (shasum -a 256|sha256sum)`", _row472p))
    _cmd472p = _cmds472p[0] if _cmds472p else None
    if not (_row472p and _vals472p and _cmd472p and _tg472p):
        _bad472p.append("Canonical text の欄に (N lines, N words, SHA-256 `…`) か再現のコマンド (sed '1,/^-\\{80\\}$/d' LICENSES/ACD-x.y.txt \\| shasum -a 256) が無い")
    else:
        _src472p = ROOT / "LICENSES" / f"{_cmd472p.group(1)}.txt"
        for _c472p in _cmds472p:
            if _c472p.group(1) != _tg472p.group(1):
                _bad472p.append(f"コマンドの本文 {_c472p.group(1)} が提出対象 {_tg472p.group(1)} でない")
        _txt472p = _src472p.read_text(encoding="utf-8") if _src472p.exists() else ""
        _ls472p = _txt472p.split("\n")
        _cut472p = next((_i for _i, _l in enumerate(_ls472p) if _l == "-" * 80), None)
        _att472p = "\n".join(_ls472p[_cut472p + 1:]) if _cut472p is not None else ""
        _n_lines472p, _n_words472p = _att472p.count("\n"), len(_att472p.split())
        _sha472p = _h472p.sha256(_att472p.encode("utf-8")).hexdigest()
        # 欄のコマンドそのものも shell で実行して照らす (2026-11-24・d7 の条件「GNU と BSD の sed で同じ値」): 上の Python の切り出しは
        #   sed の振る舞いを真似ているだけなので、欄の sed が GNU sed (CI は Linux) で同じ値を出すかは測っていなかった。mac の BSD sed
        #   では d7 と 5e が ce76f3ab… を実測済み。shasum が無い環境 (一部の Linux) では sha256sum で同じ出力を作る
        import shutil as _sh472p
        for _c472p in _cmds472p:
            # この環境に無い方の道具は、在る方で同じ出力を作る (shasum -a 256 と sha256sum は同じ 1 行を出す)
            _tool472p = _c472p.group(2)
            if not _sh472p.which(_tool472p.split()[0]):
                _tool472p = "sha256sum" if _sh472p.which("sha256sum") else "shasum -a 256"
            _cmd_shell472p = _c472p.group(0).strip("`").replace("\\|", "|").replace(_c472p.group(2), _tool472p)
            _run472p = subprocess.run(_cmd_shell472p, shell=True, cwd=ROOT, capture_output=True, text=True)
            _shell_sha472p = (_run472p.stdout.split() or [""])[0]
            if _shell_sha472p != _sha472p:
                _bad472p.append(f"欄のコマンド ({_c472p.group(2)}) を shell で実行した SHA-256 {_shell_sha472p[:12] or '(出力なし)'}… が、"
                                f"切り出しの {_sha472p[:12]}… と違う (この環境の sed が欄の形を同じに読まない)")
        if not _n_lines472p or not _n_words472p:
            _bad472p.append(f"再現のコマンドの出力が空 ({_src472p.name} に区切り線が無いか、その下が空)")
        _want472p = (int(_vals472p.group(1).replace(",", "")), int(_vals472p.group(2).replace(",", "")), _vals472p.group(3))
        if _want472p != (_n_lines472p, _n_words472p, _sha472p):
            _bad472p.append(f"欄 {_want472p[0]} 行・{_want472p[1]} 語・{_want472p[2][:12]}… / 出力 {_n_lines472p} 行・{_n_words472p} 語・{_sha472p[:12]}…")
    check(not _bad472p,
          f"Check 472p: 添付の本文の欄の行数・語数・SHA-256 が、再現のコマンドの出力と一致 (空でない)",
          f"Check 472p: {_bad472p}。添付は審査者が最初に読む本文なので、欄の値は再現のコマンドの出力そのものにする", blocking=True)
