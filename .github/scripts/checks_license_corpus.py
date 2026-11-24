"""
checks_license_corpus.py — 承認済みライセンスの母集団についての申告 (本数・census の表・誤命中の判定) を実測に照らす Check 群
(extracted from checks_license_dossier.py — check.py split track・category "corpus counts").

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES

**なぜ切り出したか**: checks_license_dossier.py が advisory (800 行) を越えた (2026-11-24・843 行)。残る側はドシエの運用の記録
(投稿先・索引・日付・在庫・停止) で、ここは「OSI 承認済みライセンスの集合を数えた値」の面 (gap-census.md と、その数を引く入口・
材料の文) だけを持つ。本文は無改変で移した。

  476. **「OSI 承認済みライセンスは N 本」という申告が、実測した版の実数であること** (BLOCKING):
       ドシエは承認済みライセンスの全数に当てた測定を何度も引く（3.28.0 で 149 本 / 3.29.0 で
       非 deprecated 141 本）。**2026-09-19 に、不利な事実の件数（#150 / #151）を上げた一括の数値
       更新が、偶然同じ値だった承認済みの本数まで 149 → 150 → 151 と押し上げていた**
       （`submission-reference.md` の 2 行・2026-09-25 に `measure_gap_claim.py` を 3.28.0 で
       再実行して発覚）。**2 つの量が偶然同じ値を持つと、片方の更新がもう片方を巻き込み、
       **476c (2026-11-06)**: 入口ページと申請日の 1 枚が述べる全数の数 (141 本 / 条件の無い 3 本 / 作品を超える
       特許許諾の 7 本) が census の表から導いた数と一致する。census を作り直した日に入口だけ古くなる形だった。
       2026-11-11 (portfolio-aa の問い): 材料表の「承認済みに無い仕掛け」の表が繰り返す数 (141 本のうち 0 本 /
       7 本はすべて条件を持つ / TDM・AI を名指す本は 0) も読み、どの面も最初の 1 か所でなく全出現を照合する。
       「名指す本は 0」は census の結論文 (`tdm` N 件・`ml` は誤命中 M 件) と誤命中の判定の行に依るので、
       その文の数が `tdm` / `ml` 列と一致し、判定の行が在ることも前提にする。
       **476d (2026-11-11)**: `measure_gap_claim.py` の向きの仕分け (estoppel / consideration / rely などが承認済みの
       本文で逆の向きに使われるのを分ける) が、承認済みの本文と ACD-1.4 草案から逐語で取った自己試験の文を
       期待どおりに仕分けること。ネットワーク無しで走る。語族ごとに ACD の向きの文を 1 つは持つこと。
       **476e (2026-11-11)**: census の「誤命中」節の判定 (`ml` は Multics の組織名、など) が、表の列 (0 でない行)・
       判定の行の列挙・生成器の `READ_MISHITS` の 3 つで同じ本の集合を指すこと。生成器は集合が違えば止まるが、
       それは取得し直した日にしか走らないので、CI で同期を見る。
       どの Check も気付かない。** 本数を名乗る数が、実測済みの版の値（`_SPDX476`）の
       どれかであることを強制する。新しい版を測ったら `_SPDX476` に足す（足すこと自体が
       「その版を実際に測った」という記録になる）。(BLOCKING)
"""
import re


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 476. 「OSI 承認済みライセンスは N 本」の申告が、実測した版の実数であること (BLOCKING) ──
    #   **量が偶然一致すると、片方の一括更新がもう片方を巻き込む。** 2026-09-19 に不利な事実の
    #   件数を 149 → 150 → 151 と上げた更新が、承認済みの本数（3.28.0 で 149）まで押し上げた。
    #   値は SPDX license-list-data を取得して数えたもの（isOsiApproved の全件 / 非 deprecated）。
    #   **新しい版を測ったら、ここに足す** —— 足さずに新しい数を書くと RED になるのは意図どおり。
    _SPDX476 = {
        "3.28.0": {149, 136},   # 全件 / 非 deprecated（deprecated ID 13）
        "3.29.0": {154, 141},   # 同上（2026-09-16 release・3.28.0 から新規承認扱い 5 件）
        "8791eda": {154, 141},  # license-list-data 既定ブランチ (2026-10-28・取得 2026-11-04・bb)。判定 141 本は 3.29.0 と同一
    }
    _ok476 = set().union(*_SPDX476.values())
    _pats476 = [
        re.compile(r"(?<![\d.,#])(\d{3})(?![\d.,])\s*(?:OSI-approved|approved licen)"),
        re.compile(r"(?:承認済み|OSI-approved|isOsiApproved)[^\d\n|]{0,12}(?<![\d.,#])(\d{3})(?![\d.,])\s*(?:本|件|licen|texts)"),
        # 2026-09-19 の実例の形: 「`isOsiApproved` 全件の本文を … | **151 件」—— 語と数の間が表のセル境界を越える
        re.compile(r"isOsiApproved[^\n]{0,80}?\*\*(\d{3})\s*件"),
    ]
    _bad476 = []
    _files476 = sorted((ROOT / "LICENSES").glob("*.md")) + sorted((ROOT / "docs" / "files" / "LICENSES").glob("*.md"))
    for _f476 in _files476:
        for _i476, _l476 in enumerate(_f476.read_text(encoding="utf-8").split("\n"), 1):
            # 第三者の逐語 (*"…"* の italic 引用) の中の数は我々の申告ではないので読まない (2026-11-15・2f の報告):
            #   Berkus 氏の *"review the over 200 approved licenses already in the OSI catalog"* を 200 本の申告と読み、
            #   逐語を省略記号で削らせていた。逐語は改変しないのが規律で、Check が引用を書き換えさせてはならない。
            #   我々自身の英文 (> の下書き・本文) は *"…"* で囲わないので、照合は残る
            _l476 = re.sub(r'\*"[^"\n]*?"\*|\*“[^”\n]*?”\*', lambda _q: " " * len(_q.group(0)), _l476)
            for _p476 in _pats476:
                for _m476 in _p476.finditer(_l476):
                    if int(_m476.group(1)) not in _ok476:
                        _bad476.append(f"{_f476.relative_to(ROOT)}:{_i476} {_m476.group(1)}")
    check(
        not _bad476,
        f"Check 476: 承認済みライセンスの本数の申告はすべて実測値 ({sorted(_ok476)}) のどれか",
        (f"Check 476: 承認済みライセンスの本数として、どの版の実測値でもない数がある: {_bad476}。"
         "**不利な事実の件数など別の量の一括更新に巻き込まれていないか**を先に疑え "
         "(2026-09-19 に 149 → 150 → 151 の実例)。新しい SPDX 版を実際に測ったなら "
         "`_SPDX476` にその版と値を足せ"),
        blocking=True,
    )
    # 476c —— 入口ページと申請日の 1 枚が述べる全数の数が、census の表から導いた数と一致する (2026-11-06)。
    #   476b は §1.133 の表しか見ない。審査者が読む 2 面の文は census と照合されておらず、census を作り直した
    #   日に入口だけ古くなる。数は語で書かれているので語も読む (portfolio-00 の提案)。
    _cs476c = ROOT / "LICENSES" / "ACD-1.0.gap-census.md"
    _rv476c = ROOT / "LICENSES" / "REVIEWERS.md"
    _sm476c = ROOT / "LICENSES" / "SUBMISSION-MATERIALS.md"
    if _cs476c.exists() and _rv476c.exists() and _sm476c.exists():
        _ct476c = _cs476c.read_text(encoding="utf-8")
        _rows476c = [_l.split("|") for _l in _ct476c.split("\n") if _l.startswith("| `")]
        _n476c = len(_rows476c)
        _b476c = sum(_r[5].strip() in ("S2", "S3") for _r in _rows476c if len(_r) > 5)
        _m476c = re.search(r"公有等価の (\d+) 本（([^）]+)）", _ct476c)
        _z476c = len(re.findall(r"`[^`]+`", _m476c.group(2))) if _m476c else -1
        _w476c = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
        _rt476c = " ".join(_rv476c.read_text(encoding="utf-8").split())
        _st476c = " ".join(_sm476c.read_text(encoding="utf-8").split())
        # 語の列 (tdm / ml) は「0 は空欄」。0 でない行の数を数える
        _col476c = lambda _k: sum(1 for _r in _rows476c if len(_r) > _k and _r[_k].strip() not in ("", "0"))
        _tdm476c, _ml476c = _col476c(6), _col476c(7)
        _bad476c = []
        # 「名指す本は 0」は census の結論文に依る。結論文の数が列と一致し、ml の誤命中を判定した行が在ること
        #   (portfolio-aa・2026-11-11): 生成器はこの文を固定の形で書くので、列が動いても文は 0 のまま残りうる
        _cc476c = re.search(r"\*\*(\d+) 本のうち、TDM・データマイニング・機械学習・AI を名指しする本は (\d+) 本\*\*"
                            r"（`tdm` (\d+) 件・`ml` は誤命中 (\d+) 件のみ）", _ct476c)
        _mj476c = re.search(r"^- `ml` の (\d+) 件 —— \S", _ct476c, re.M)
        if not _cc476c or [int(_x) for _x in _cc476c.groups()] != [_n476c, _tdm476c, _tdm476c, _ml476c]:
            _bad476c.append(f"census の (a) の結論文: 述べる {_cc476c.groups() if _cc476c else '文が無い'} / "
                            f"表 ({_n476c}, {_tdm476c}, {_tdm476c}, {_ml476c})")
        if _ml476c and not (_mj476c and int(_mj476c.group(1)) == _ml476c):
            _bad476c.append(f"census の誤命中: `ml` の {_ml476c} 件を判定した行が無い")
        # どの面も全出現を照合する (2026-11-11): search は最初の 1 か所しか見ず、材料表が同じ数を別の行で
        #   繰り返すと (「承認済みに無い仕掛け」の表)、繰り返しの側は census を作り直しても古いまま残った
        for _label, _pat, _text, _want in (
                ("REVIEWERS の全数", r"Of the \*\*(\d+) licences", _rt476c, _n476c),
                ("REVIEWERS の条件ゼロ", r"exactly (\w+) impose no condition", _rt476c, _z476c),
                ("REVIEWERS の作品を超える本数", r"(\w+) extend a patent grant beyond the work itself", _rt476c, _b476c),
                ("REVIEWERS の条件つきの本数", r"all (\w+) carry a condition", _rt476c, _b476c),
                ("材料表の全数", r"承認済みライセンスは、? ?(\d+) 本のうち", _st476c, _n476c),
                ("材料表の作品を超える本数", r"作品を超える特許許諾を持つ (\d+) 本", _st476c, _b476c),
                ("材料表の条件ゼロ", r"条件ゼロの承認済み (\d+) 本", _st476c, _z476c),
                ("材料表の「N 本のうち」の N", r"(\d+) 本のうち \d+ 本", _st476c, _n476c),
                ("材料表の条件の無い作品を超える許諾", r"\d+ 本のうち (\d+) 本", _st476c, 0),
                ("材料表の「すべて条件を持つ」本数", r"(\d+) 本はすべて条件を持つ", _st476c, _b476c),
                ("材料表の「承認済み N 本で」", r"承認済み (\d+) 本で", _st476c, _n476c),
                ("材料表の TDM・AI を名指す / 留保に触れる本", r"(?:名指す|触れる)本[はも] \**(\d+)\**", _st476c, _tdm476c)):
            _gs = list(re.finditer(_pat, _text, re.I))
            _vs = [int(_g.group(1)) if _g.group(1).isdigit() else _w476c.get(_g.group(1).lower()) for _g in _gs]
            if not _vs or any(_v != _want for _v in _vs):
                _bad476c.append(f"{_label}: 述べる {[_g.group(1) for _g in _gs] or '文が無い'} / census {_want}")
        check(
            _z476c > 0 and not _bad476c,
            f"Check 476c: 入口と材料表の全数の数が census の表と一致 ({_n476c} 本 / 条件ゼロ {_z476c} / 作品を超える {_b476c} / "
            f"TDM・AI を名指す {_tdm476c}・ml の誤命中 {_ml476c})",
            (f"Check 476c: 入口または材料表の数が census と違う: {_bad476c or 'census の公有等価の文が読めない'}。"
             "census を作り直したら審査者が読む 2 面も同じ commit で直せ"),
            blocking=True,
        )
    # 476b —— B10 の立証 (gap-measurements.md §1.133) の分割の内訳が、census の表から導いた数と一致する (2026-11-04)。
    #   §1.133 は 141 本を「P0 明示の特許許諾なし / P1 S1 / P2 S2 / P3 S3」に分け、各組が「範囲・無条件・終了なし」の
    #   どれを欠くかで立証する。数は census の表から導かれる派生値なので、census を生成し直して分類が動けば、
    #   立証の数字だけが黙って古くなる (476 が本数を実測の版に縛るのと同じ理由の、内訳版)。
    _gm476b = (ROOT / "LICENSES" / "ACD-1.0.gap-measurements.md")
    _cs476b = (ROOT / "LICENSES" / "ACD-1.0.gap-census.md")
    if _gm476b.exists() and _cs476b.exists():
        _rows476b = [_l.split("|") for _l in _cs476b.read_text(encoding="utf-8").split("\n") if _l.startswith("| `")]
        _sc476b = [(_r[5].strip() if len(_r) > 5 else "") for _r in _rows476b]
        _want476b = {"P0": len(_rows476b) - sum(_x in ("S1", "S2", "S3") for _x in _sc476b),
                     "P1": _sc476b.count("S1"), "P2": _sc476b.count("S2"), "P3": _sc476b.count("S3")}
        _gt476b = _gm476b.read_text(encoding="utf-8")
        _sec476b = _gt476b[_gt476b.find("## 1.133"):]
        _got476b = {m.group(1): int(m.group(2)) for m in re.finditer(r"^\| (P[0-3]) [^|]*\| (\d+) \|", _sec476b, re.M)}
        check(
            _got476b == _want476b,
            f"Check 476b: §1.133 の分割の内訳 {_got476b} が census の表と一致",
            (f"Check 476b: §1.133 の分割の内訳 {_got476b} が census の表から導いた {_want476b} と一致しない "
             "(census を生成し直して分類が動いたか、§1.133 の表を手で書き換えた)。立証の根拠の数なので、"
             "census の分類を確かめてから §1.133 を合わせよ"),
            blocking=True,
        )
    # 476d —— measure_gap_claim.py の向きの仕分けが、自己試験の文を期待どおりに仕分ける (2026-11-11)。
    #   材料表 §1c は「承認済みの本文にも在るが逆の向き」(estoppel は黙示の許諾を否定する列挙に、consideration は
    #   条件の対価に) を述べ、この道具の仕分けで再現できる。仕分けは正規表現なので、変えたときに向きが
    #   入れ替わっても数は「それらしい数」のまま出る。承認済みの本文と ACD-1.4 草案から逐語で取った文を、
    #   ネットワーク無しで仕分けて確かめる。語族ごとに ACD の向きの文を 1 つは持つことも見る
    import contextlib as _cl476d
    import importlib.util as _iu476d
    import io as _io476d
    _out476d = _io476d.StringIO()
    try:
        _sp476d = _iu476d.spec_from_file_location("_mgc476d", ROOT / ".github" / "scripts" / "measure_gap_claim.py")
        _md476d = _iu476d.module_from_spec(_sp476d)
        _sp476d.loader.exec_module(_md476d)
        with _cl476d.redirect_stdout(_out476d):
            _rc476d = _md476d.self_test()
        _acd476d = {_f for _t, _f, _w in _md476d._SELF_TEST if _w.startswith("ACD's direction")}
        _lack476d = [_n for _n, *_r in _md476d.DIRECTED if _n not in _acd476d]
    except Exception as _e476d:  # noqa: BLE001 — 読めないことも RED
        _rc476d, _lack476d = 2, []
        _out476d.write(f"{type(_e476d).__name__}: {_e476d}")
    _last476d = (_out476d.getvalue().strip().splitlines() or [""])[-1]
    check(
        _rc476d == 0 and not _lack476d,
        f"Check 476d: measure_gap_claim.py の向きの仕分けが自己試験の文を期待どおりに仕分ける ({_last476d})",
        (f"Check 476d: measure_gap_claim.py の向きの仕分けが崩れている: {_out476d.getvalue().strip()[:400]}"
         + (f" / ACD の向きの自己試験の文が無い語族: {_lack476d}" if _lack476d else "")
         + "。材料表 §1c が引く「逆の向き」の数は、この仕分けで出る。正規表現を変えたら自己試験の文が同じ向きに落ちることを確かめよ"),
        blocking=True,
    )
    # 476e —— census の「誤命中」節の判定が、表の列と生成器の READ_MISHITS と同じ本の集合を指す (2026-11-11)。
    #   census の (a) / (c) の結論文 (「AI を名指しする本は 0 本」「モデル・パラメータを名指しする許諾は 0 本」) と
    #   誤命中の判定の文は、生成器が固定の文で書く。生成器は命中の集合が READ_MISHITS と違えば止まるが、それは
    #   取得し直した日にしか走らない。ここでは census の表の列 (0 でない行)・判定の行の列挙・READ_MISHITS の
    #   3 つが同じ集合であることを CI で見る (art4 は表の列が無いので、判定の行と READ_MISHITS の 2 つ)
    import ast as _ast476e
    _cs476e = ROOT / "LICENSES" / "ACD-1.0.gap-census.md"
    _gn476e = ROOT / ".github" / "scripts" / "generate_gap_census.py"
    _bad476e, _read476e = [], {}
    try:
        for _nd in _ast476e.walk(_ast476e.parse(_gn476e.read_text(encoding="utf-8"))):
            if isinstance(_nd, _ast476e.Assign) and any(getattr(_t, "id", "") == "READ_MISHITS" for _t in _nd.targets):
                for _k, _v in zip(_nd.value.keys, _nd.value.values):
                    _read476e[_ast476e.literal_eval(_k)] = (set() if isinstance(_v, _ast476e.Call)
                                                            else set(_ast476e.literal_eval(_v)))
    except (OSError, SyntaxError, ValueError, AttributeError) as _e:
        _bad476e.append(f"生成器の READ_MISHITS が読めない ({type(_e).__name__})")
    _ct476e = _cs476e.read_text(encoding="utf-8") if _cs476e.exists() else ""
    _rows476e = [_l.split("|") for _l in _ct476e.split("\n") if _l.startswith("| `")]
    _col476e = {"tdm": 6, "ml": 7, "train": 8, "model": 9, "param": 10}
    for _k in ("tdm", "ml", "train", "model", "param", "art4"):
        _sets = {}
        if _k in _col476e:
            _sets["表の列"] = {_r[1].strip().strip("`") for _r in _rows476e
                              if len(_r) > _col476e[_k] and _r[_col476e[_k]].strip() not in ("", "0")}
        _mj = re.search(r"^- `" + _k + r"` の (\d+) 件 —— (.*?): ", _ct476e, re.M)
        if _mj:
            _sets["誤命中の行"] = set(re.findall(r"`([^`]+)`", _mj.group(2)))
            if int(_mj.group(1)) != len(_sets["誤命中の行"]):
                _bad476e.append(f"{_k}: 誤命中の行が {_mj.group(1)} 件と述べて {len(_sets['誤命中の行'])} 本を挙げる")
        elif _k != "tdm":
            _bad476e.append(f"{_k}: census に誤命中の判定の行が無い")
        if _k not in _read476e:
            _bad476e.append(f"{_k}: 生成器の READ_MISHITS に無い")
        else:
            _sets["READ_MISHITS"] = _read476e[_k]
        if len({frozenset(_v) for _v in _sets.values()}) > 1:
            _bad476e.append(f"{_k}: " + " / ".join(f"{_n} {sorted(_v)}" for _n, _v in _sets.items()))
    check(
        not _bad476e,
        f"Check 476e: census の誤命中の判定が、表の列と生成器の READ_MISHITS と同じ本を指す ({', '.join(f'{_k} {len(_v)}' for _k, _v in _read476e.items())})",
        (f"Check 476e: census の誤命中の判定と表・生成器が食い違う: {_bad476e}。(a) / (c) の結論文は読んだ集合を固定の文で書くので、"
         "集合が変わったら本文を読み直し、結論文・判定の文・READ_MISHITS を同じ commit で直せ"),
        blocking=True,
    )
