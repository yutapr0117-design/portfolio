"""
checks_license_quotation.py — ドシエが引く語が、引いた先に実在することを見る Check
(extracted from checks_license_dossier.py — check.py split track・category "quotation fidelity").

このモジュールが持つ invariant は 1 つ: **引用符の中身は、帰属先に実在する。**

ドシエは審査者に「本文を当たれ」と言う文書である。その本文の語を引くとき、引用が当の条項に
無ければ、審査者は**我々が読んでいない条項について論じている**と読む。しかもこの class の
欠陥は視覚にも behavior e2e にも出ず、`check_deployed_freshness.py` にも出ない ——
**引用の忠実性だけを見る層が無ければ、どの層も見ていない。**

**外部 source の引用（審査者の発言）は別の道具が持つ** ——
`.github/scripts/verify_dossier_quotations.py` が公開アーカイブを取得して照合する。
そちらは**外部フォーラムへ fetch するので CI に載せない**（脆い）。本モジュールが見るのは
**リポジトリ内に凍結されている ACD-1.0 本文**だけなので、offline で決定的に検証できる。

**分割の理由**: 2026-09-14 に Check 470 を足した時点で `checks_license_dossier.py` が
advisory (800) を越えた。**圧縮で誤魔化さず、いま触っているクラスタを切り出す**
（`checks_mutation_integrity.py` / `checks_license_self_reporting.py` と同じ手）。

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/warnings by reference (exec 不使用) so append
semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  470. **ライセンス本文の語を、それが実在しない条項に帰属させないこと** (BLOCKING):
       見るのは**証明できる取り違えだけ** —— 引用された語句が ACD-1.0 の**どの条項に在るかが
       一意に決まる**とき、同じ段落が挙げる条番号のどれもその条項を含まないなら RED。
       語句がライセンス本文でないもの（審査者の発言・我々自身の英文・1.1 草案の案文）は
       **そもそも母数に入らない**ので、帰属を推測する必要がない。母数は実測 112 件。
       ⚠ **射程を正直に書く** (#1172): 2026-09-14 の敵対的検証（主張の種類 5）が出した
       実欠陥 5 件のうち、**本 Check が捕捉するのは 1 件だけ**である
       （`AS-OF.md` が法への参照規則を §15.6 に帰属＝実体 §15.2）。残る 4 件は
       **掃引が見つけたのであって gate が見つけたのではない**:
       提出文書側の同じ取り違え（同じ段落が §15.2 も挙げるため covered と判定される）/
       "reformed to the minimum extent" の §15.2↔§15.4 / §16.4 を "continues" と引用
       （実体 "continue"）/ §10.5・§11.3・§11.4 が **each**
       "not a condition upon Your use of the Work" と言うと記述（**全文に 0 回**）。
       **より広い形は測ったうえで採らなかった**（#977 / #1212 と同じ判断）: 帰属の近さで
       当てる形は母数 26・誤検出 0 だが**実欠陥を 1 件も捕捉しない**。「同じ文に条項参照と
       英語引用があれば当てる」形は母数 107 中 35 件が RED になり、その大半が**正当な記述**
       だった。**正当な記述を RED にする gate は、正しい書き方を避けさせる分だけ害がある。**
       **470b (2026-11-23・6d の依頼・fc)**: 外向きの文書 (`_OUTWARD470B`) の *"…"* の片 (4 語以上・… で割る) で、どの版の本文
       (`ACD-1.*.txt`・草案・`CHANGES-ACD-*.txt`) にも逐語で無く (句読点と大小を外しても無く)、3 語連鎖の 85% 以上が本文に在り、
       前後 40 字に試作の番号 (T と数字) が無いものを RED にする。本文をほぼそのまま引いたのに語がずれた形 = 古い草案の文を
       「いまの文」として引いた形である。470 は「どこかの版に在る語」しか母数に入れないので、この形は見えなかった
       (cd が #3899 で submission-reference §4.4 と逐条 §12.5 の 2 件を手で見つけた)。T 番号を添えた引用は試作の歴史として
       外す (逐条は「T115 の前は *"…"*」の形で途中の草案を引く)。errata・against・試作の冊は途中の草案を歴史として引くので
       対象外。導入時の実測: 1,829 片のうち 1 件 (逐条 §8.4 の行・T99 より前の §8.3 第 2 文) で、同じ commit で直した。
       2026-11-27 (72 の報告・d7): 1 行ずつ探していたので、行をまたぐ *"…"* を 1 片も見ていなかった。段落の中 (空行をまたがない)
       で拾う形にし、見える片は 794 → 934。増えた片で REVIEWERS の "ACD-1.4 §1.7" (確定前の草案の語・#4273 で直した) と
       QUESTIONS-FOR-COUNSEL §12.3 (1.3 の文に 1.4 草案の複数形の動詞を継いだ・72 が #4277 で直した) の 2 件が出た。**作らなかったもの**: 「ACD-1.N と
       名乗る引用がその版に在るか」(72・7e の依頼)。名乗りを前 90 字の ACD-1.N で取ると 65 片中 19 件で本物は REVIEWERS の 1 件
       (残りは file 名・他のライセンス・第三者の引用)、名乗りを隣接の形に絞ると 26 片中 0 件で REVIEWERS 自体を落とす。
       **470c (2026-11-24・cd の #4029 と 5e の提案・fc・BLOCKING)**: 外向きの文書 (`_OUTWARD470B` に register と ADOPTING を足す)
       の *"…"* で、Dedicator / Dedication / the Work / Section N のどれかを含み、提出対象の版 (SUBMISSION-TARGET) の本文に無く、
       それより前の版 (1.0〜) のどれかの本文に在るものを数える。前後に版の名 (1.0〜1.3) か経緯の印 (外し・旧・was・formerly 等)
       があれば外す。470b は「どの版にも無い語のずれ」を見るので、**前の版に逐語で在る文を版を名乗らずに現在形で引く**形
       (提出対象を 1.4 へ切り替えた後の against #110・B10 の §6.4) は見えなかった。cd は経緯の文の判定が粗いので ADVISORY を勧めたが、
       BLOCKING にした: ADVISORY は ::error:: を出さないので mutation の probe が捕捉を測れず (479d が名指しの mutation を求める)、
       直し方は安い (版を名乗る "in ACD-1.0" を 1 句足す)。誤検出が出たら、印の語を足すか ADVISORY へ戻す。
       **射程 (緑の読み方・6d の依頼)**: 印の語は前後 250 / 150 字の正規表現で探すので、近くに別の文の印 (旧・was・1.0 の名など) が
       あると現在形の誤りを見逃す。誤りは見逃しの側にしか出ない。**470c が緑でも「外向きの引用は全部 1.4 の文」とは読めない** ——
       Dedicator / Dedication / the Work / Section N を含まない引用と、どの版にも無い引用 (470b の担当) も母数の外である。
       **作業中の草案 (いまは 1.5) の語は設計として対象外** (5e の問い): 草案の語は提出対象にも前の版にも無いので当たらないが、
       それは偶然ではなく、草案の語は「1.5 草案」の印で名乗る (468a が草案に当てる) という分担である。草案を確定して提出対象を
       切り替えた日に、その語は提出対象の本文に入るので、470c は何もしなくてよい。
       2026-11-27 (d7・470b と同じ穴): 1 行ずつ探していたので行をまたぐ *"…"* を見ていなかった。段落の中で拾い (219 → 250 件)、
       片の先頭 1 字の大小を区別しない (文頭の "So far as" を文の途中で小文字で引く慣行で偽の 1 件が出た)。印を探す窓は同じ段落の
       中の前 250 字・後 150 字 (旧版の「同じ行」は折り返しの偶然に依る)。増えた 31 件に前の版を名乗らない引用は無かった。
       **地の文は拾わない** (d7 の問い): 見るのは斜体の *"…"* だけで、引用符の無い地の文の古い語 (#4007 や想定問答の
       "Section 8.4 deliberately reaches only claims …" の形) は母数の外。地の文は確定の日に `prepare_version_freeze.py --report`
       の「同じ番号で書き直した条」の節で人が読む、という分担である。
       導入時の実測: 12 冊の引用 201 件のうち 0 件 (cd が against #110 を直した後・SUBMISSION-MATERIALS の経緯の文 1 件は印の語「外し」で外れる)。

  505. **委員長でなかった時期の発言者を「委員長」「chair」と書かないこと** (BLOCKING・2026-11-25・議題 33):
       決める側の誰が、どの資格で言ったかは重みを変える (against #186)。2026-10 に約 115 か所を直した型が、提出の材料 2 か所で再発した
       (#4148)。逆向き (委員長だった月の発言者を「元」「のちの」と書く) も見る。役・名・発言日が隣り合う 3 つの形だけを見る。
       作った日の母数: LICENSES/*.md と docs/files/LICENSES/**/*.md (rounds/ の受領文の mirror を含む) で、拾った文は全部読んで真 5・
       誤検出 0 (拾った数は OK 行に出す)。否定 (委員長ではない)・「」の言及・別人の括弧の中の委員長では鳴らないことを対照で確かめた。
       2026-11-26: 英語の形 (`, chair, on` / `as chair, license-review DATE` / `(Licensing Committee chair, DATE)` /
       `the committee chair`) を足した。拾う文は 39 → 45 で、増えた 6 文は全部在任中で正しかった (誤検出 0)。
       **逆側**: 日付の離れた文と名の無い「委員長は」は見えない (2 件はそれで手で見つけた)。在任の表は記録に
       依るので、委員長が替わった日に `_lib_dossier.CHAIR_TERMS` を直さないと偽 RED になる。境目の月は止めない。対象が減る形は件数の下限。
       2026-11-27: Nelson 氏 (2003-05〜2010-12) を表に足した (d7・census_board_self_identification.py の本人の報告の語)。拾う文は
       62 → 87 で、足した日に RED になったのは 2002 年の Nelson 氏を「委員長」と書いた 2 行だけ (委員会は 2003-04 に作られた・
       同じ commit で「承認の窓口」へ直した)。日付の離れた外向きの英語 3 か所 ("committee chair said in 2002" ほか) は手で直した。
"""

import re


def run(ctx):
    """Run the quotation-fidelity Checks. ctx carries shared check()/ROOT by reference."""
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 470. ライセンス本文の語を、それが実在しない条項に帰属させないこと (BLOCKING) ────
    # ドシエは審査者に「本文を当たれ」と言う文書である。**条項を指す矢印が、指した先に
    # 無いものを述べていれば、審査者は我々が読んでいない条項について論じていると読む。**
    #
    # 本 Check が見るのは**証明できる取り違えだけ**である: 引用された語句が ACD-1.0 の
    # **どの条項に在るかが一意に決まる**とき、同じ段落が挙げる条番号のどれもその条項を
    # 含まないなら RED。語句がライセンス本文でないもの（審査者の発言・我々自身の英文・
    # 1.1 草案の案文）は**そもそも母数に入らない**ので、帰属の推測が要らない。
    #
    # ⚠ **射程を正直に書く** (#1172 の規律)。2026-09-14 の敵対的検証 (主張の種類 5) は
    # 実測 5 件の欠陥を出したが、**本 Check が捕捉するのはそのうち 1 件だけ**である
    # （AS-OF.md が法への参照規則を §15.6 に帰属＝実体 §15.2）。残る 4 件 ——
    # 提出文書側の同じ取り違え（同じ段落が §15.2 も挙げるため covered と判定される）/
    # "reformed to the minimum extent" の §15.2↔§15.4 / §16.4 を "continues" と引用
    # （実体 "continue"）/ §10.5・§11.3・§11.4 が **each** "not a condition upon Your use
    # of the Work" と言うと記述（**この語句は全文に 0 回**）—— は**掃引が見つけたのであって
    # gate が見つけたのではない**。
    #
    # **より広い形は測ったうえで採らなかった** (#977 / #1212 と同じ「Check にしない判断も
    # 成果物」): 帰属の近さで当てる形は母数 26 で誤検出 0 だが**実欠陥を 1 件も捕捉せず**、
    # 「同じ文に条項参照と英語引用があれば当てる」形は母数 107 中 35 件が RED になり、その
    # 大半が**正当な記述**だった。**正当な記述を RED にする gate は、正しい書き方を
    # 避けさせる分だけ害がある。**
    _lic470 = ROOT / "LICENSES" / "ACD-1.0.txt"
    if _lic470.exists():
        def _norm470(_t):
            _t = _t.replace("\u201c", '"').replace("\u201d", '"').replace("\u2019", "'")
            return re.sub(r"\s+", " ", _t).lower()

        # 条項の境界は**行頭 2 空白**で決まる。本文は 7 空白の字下げなので、折り返し行が
        # "8.3 rejects…" で始まっても条項見出しには見えない（初版はこれを取り違え、§8.3 の
        # 本文を §8.4 の途中から取り、**正しい引用を「実在しない」と報告しかけた**）。
        def _clauses470(_path):
            # 条は次の条か、節の見出し (`11. TRADEMARKS…`) か END OF TERMS で切る。見出しで切らないと、節の見出しの語が
            #   前の条の語に数えられる (版の地図を足したとき §10.5 に "TRADEMARKS, NAMES, …" が入って誤検出した)
            _ls = _path.read_text(encoding="utf-8").split("\n")
            _st = [(_m.group(1), _n) for _n, _l in enumerate(_ls) for _m in [re.match(r"^  (\d{1,2}\.\d{1,2})\s", _l)] if _m]
            _hd = [_n for _n, _l in enumerate(_ls) if re.match(r"^\d{1,2}\. [A-Z]|^END OF TERMS", _l)]
            def _end(_n, _nx):
                return min([_h for _h in _hd if _n < _h < _nx] + [_nx])
            return {_c: _norm470("\n".join(_ls[_n:_end(_n, _st[_k + 1][1] if _k + 1 < len(_st) else len(_ls))]))
                    for _k, (_c, _n) in enumerate(_st)}
        _clause470 = _clauses470(_lic470)
        # 版を名乗る段落は、その版の本文の条の地図で照らす (2026-11-16・30 の報告): 1.0 と 1.1 以降は §1 と §15・§16 の
        #   番号の中身が違い (1.0 の §1.3 = "Dedicator" は 1.4 草案の §1.4)、1.4 草案の §1.4 を正しく引いた段落を、1.0 の地図で
        #   「§1.3 の語を §1.4 に帰属させた」と誤って RED にした。名乗りは段落の中の「1.N 草案 / 1.N draft / ACD-1.N」
        _vers470 = {"1.0": _clause470}
        for _vp in sorted((ROOT / "LICENSES").glob("ACD-1.[1-9].txt")):
            _vers470[_vp.stem.split("-")[1]] = _clauses470(_vp)
        for _vp in sorted((ROOT / "LICENSES").glob("ACD-1.[1-9]-DRAFT.txt")):
            if "HAS BEEN FROZEN" not in _vp.read_text(encoding="utf-8").split("\n", 1)[0]:
                _vers470[_vp.stem.split("-")[1]] = _clauses470(_vp)
        # 名乗りは明示の形だけ (ACD-1.N / 1.N 草案 / 1.N draft / version 1.N)。裸の「1.1」は「§11.1」の中にも在り、1.0 の番号で
        #   書いた表を 1.1 の地図で照らして誤検出した (AUDIT-LEDGER の表・2026-11-16)
        _verrx470 = re.compile(r"(?<![\d.§])(?:ACD-1\.([1-9])(?![\d\-])|1\.([1-9])\s*(?:草案|draft)|version 1\.([1-9])(?!\d))")

        _sec470 = re.compile(r"\u00a7\s?(\d{1,2}(?:\.\d{1,2})?)(?![0-9a-zA-Z.])")
        _q470 = re.compile(r'\*"([^"]{6,300})"\*|"([A-Za-z][^"\u201c\u201d]{8,300})"|\u201c([^\u201d]{8,300})\u201d')
        _bad470, _pop470 = [], 0
        for _f470 in sorted((ROOT / "LICENSES").glob("*.md")):
            _lines470 = _f470.read_text(encoding="utf-8").split("\n")
            # 段落（空行で区切られた行の塊）を 1 つの主張の文脈とする。**行単位では折り返しで
            # 条番号が前の行に落ち、正しい記述を誤検出する**（実測 1 件）。
            _paras470, _buf470 = [], []
            for _n470, _l470 in enumerate(_lines470, 1):
                if _l470.strip():
                    _buf470.append((_n470, _l470))
                elif _buf470:
                    _paras470.append(_buf470)
                    _buf470 = []
            if _buf470:
                _paras470.append(_buf470)
            for _blk470 in _paras470:
                _txt470 = "\n".join(_l for _, _l in _blk470)
                _refs470 = {_m.group(1) for _m in _sec470.finditer(_txt470)}
                if not _refs470:
                    continue
                # 版を名に持つ作業の文書 (ACD-1.4-…-TRIAL・CHANGELIST など) は自分の節にも § を振る (§14.22) ので、条の番号と
                #   区別できない。版の地図はそれ以外の文書 (1.0 のドシエと入口) の、版を 1 つだけ名乗る段落に当てる
                # 引用の中の語は名乗りに数えない ("LicenseRef-ACD-1.1 while …" を引いた段落が 1.1 を名乗ったことになった)
                _named470 = ({f"1.{next(_g for _g in _m.groups() if _g)}" for _m in _verrx470.finditer(_q470.sub(" ", _txt470))}
                             & set(_vers470)
                             if not re.match(r"ACD-1\.[1-9][.-]", _f470.name) else set())  # 確定した版の文書 (ACD-1.4.…) も同じ扱い (2026-11-23)
                # 1.0 の地図と、名乗った版の地図のどれかで帰属が合えば良しとする (置き換えると、1.0 の番号で引きながら後の版も
                #   名乗る register の行を誤検出した)。どの地図でも合わないときだけ RED
                _maps470 = [_clause470] + [_vers470[_v] for _v in sorted(_named470) if _v != "1.0"]
                # ACD-1.N- の作業文書は、そのファイル名の版の地図でも帰属を受ける (2026-11-20・2f の案: 1.4 草案の §1.4 を正しく引いた
                #   UNIQUE-READING の行が、1.0 の地図だけで照らされて「§1.3 の語」と出ていた)。ただし母数 (どの引用を照らすか) は
                #   今までどおり 1.0 と名乗った版の地図で決める —— 作業文書は自分の節にも § を振る (§14.22) ので、草案にだけ在る
                #   引用まで照らすと、節の番号を条の番号と取り違えて誤検出する (2026-11-18 に地図を置き換えて 19 件が出た)
                # 確定した版の文書 (ACD-1.4.clause-reference.md・版の後がドット) も、その版の地図で帰属を受ける (2026-11-23: 逐条を
                #   改名したら、1.4 の番号で正しく書いた §2.4・§16.6 の 2 件を 1.0 の地図だけで照らして誤検出した・5e の報告)
                _fv470 = re.match(r"ACD-(1\.[1-9])[.-]", _f470.name)
                _accept470 = _maps470 + ([_vers470[_fv470.group(1)]] if _fv470 and _fv470.group(1) in _vers470 else [])
                # 版 N の作業文書 (試作・CHANGELIST) は直前の凍結版の条を論じる。1.5 は番号を総替えしたので、1.4 の番号で正しく引いた
                #   行が 1.0 と 1.5 の地図だけで照らされて誤検出した (2026-11-24・議題 16)
                if _fv470:
                    _pv470 = f"1.{int(_fv470.group(1).split('.')[1]) - 1}"
                    _accept470 += [_vers470[_pv470]] if _pv470 in _vers470 and _pv470 != "1.0" else []
                def _cov_of470(_m):
                    _c = set()
                    for _r470 in _refs470:
                        _c.add(_r470)
                        if "." not in _r470:  # \u00a715 は \u00a715.2 を覆う
                            _c |= {_k for _k in _m if _k.startswith(_r470 + ".")}
                    return _c
                for _n470, _l470 in _blk470:
                    for _qm470 in _q470.finditer(_l470):
                        _quote470 = re.sub(r"\*\*|\\", "", next(_g for _g in _qm470.groups() if _g))
                        if len(_quote470.split()) < 5 or not re.search(r"[A-Za-z]{3}", _quote470):
                            continue
                        _nq470 = re.sub(r"[.,;:]+$", "", _norm470(_quote470)).strip()
                        _owns470 = [({_k for _k, _v in _m.items() if _nq470 in _v}, _cov_of470(_m)) for _m in _accept470]
                        _own470 = next((_o for _o, _c in _owns470[:len(_maps470)] if _o), set())
                        if not _own470:
                            continue  # \u30e9\u30a4\u30bb\u30f3\u30b9\u672c\u6587\u3067\u306a\u3044\u3082\u306e\u306f\u6bcd\u6570\u5916
                        _pop470 += 1
                        if not any(_o & _c for _o, _c in _owns470):
                            _bad470.append(
                                f"{_f470.name}:{_n470} \u5f15\u7528\u306f \u00a7{sorted(_own470)[0]} \u306e\u8a9e\u3060\u304c\u3001"
                                f"\u6bb5\u843d\u304c\u6319\u3052\u308b\u306e\u306f \u00a7{sorted(_refs470)[:4]}: \"{_quote470[:70]}\"")
        check(
            not _bad470,
            f"Check 470: \u672c\u6587\u306e\u8a9e\u3092\u5f15\u3044\u305f {_pop470} \u4ef6\u304c\u3001\u305d\u308c\u304c\u5b9f\u5728\u3059\u308b\u6761\u9805\u3092\u6319\u3052\u3066\u3044\u308b",
            (f"Check 470: \u30e9\u30a4\u30bb\u30f3\u30b9\u672c\u6587\u306e\u8a9e\u3092\u3001\u305d\u308c\u304c\u5b9f\u5728\u3057\u306a\u3044\u6761\u9805\u306b\u5e30\u5c5e\u3055\u305b\u3066\u3044\u308b: {_bad470}\u3002"
             "**\u30c9\u30b7\u30a8\u306f\u5be9\u67fb\u8005\u306b\u300c\u672c\u6587\u3092\u5f53\u305f\u308c\u300d\u3068\u8a00\u3046\u6587\u66f8\u3067\u3042\u308b\u3002**"
             "\u6761\u756a\u53f7\u3092\u76f4\u3059\u304b\u3001\u305d\u306e\u6bb5\u843d\u3067\u5b9f\u969b\u306b\u8ad6\u3058\u3066\u3044\u308b\u6761\u9805\u3092\u6319\u3052\u3088"),
            blocking=True,
        )
        # 470 の問いの引用の枝 (ADVISORY・2026-11-16・下位部の番号は振らない: probe は ADVISORY を RED と数えないので、名指す mutation を作れない): 法律家と実務家への問いは 1.4 草案の条番号で書かれ、草案の文を逐語で引く。試作で草案の文が
        #   変わると、問いが古い文を「1.4 草案は」として引いたままになる (T80・T92・T93 の後に 5 件・9b の測定)。470 は 1.0 の
        #   地図で合えば通すので鳴らない。引用の断片 (5 語以上) が草案に逐語で無く、どれかの ACD の本文と 5 語の連なりを 4 割以上
        #   共有する (= ACD の文の引用で、外の法源や発言の引用ではない) ものを数える。段落のその引用より前が旧版を名乗れば除く
        # 本体は _lib_draft_counts.stale_draft_quotes (2026-11-20: list_open_items が帯の人へ出すために同じ数え方を使う)
        from _lib_draft_counts import stale_draft_quotes
        _stale470b = [f"{_f}: \"{_fr[:70]}\"" for _f, _head, _fr in stale_draft_quotes(ROOT)]
        check(
            not _stale470b,
            "Check 470 (問いの引用・ADVISORY): 法律家と実務家への問い・逐条リファレンス・一意に定める記録が引く草案の文は、いまの草案に逐語で在る",
            (f"Check 470 (問いの引用・ADVISORY): 問いが、いまの草案に無い ACD の文を引いている（試作で文が変わったか、言い回しがずれた）: "
             f"{_stale470b}。草案の文に揃えるか、旧版の文なら段落のその引用より前で版を名乗れ"),
            blocking=False,
        )
        _selfquote_470b(ROOT, check)
        _target_version_470c(ROOT, check)
    else:
        # 対象が無いのに黙って skip しない (2026-11-02): 改名・移動を正しく済ませると他の Check は全部緑のまま、
        # ここだけが OK も ERROR も出さずに消える (460 / 469 で踏んだ形)。
        check(False, "Check 470: 対象ファイル",
              f"Check 470: 検査対象 {_lic470.relative_to(ROOT).as_posix()} が無い —— 改名・移動したならこの Check の参照先を直す (黙って skip しない)")


def _target_version_470c(ROOT, check):
    """470c の本体 (docstring の 470c)。返り値なし。"""
    from _lib_dossier import submission_target_version
    L = ROOT / "LICENSES"
    tv = submission_target_version(L)
    norm = lambda s: " ".join(s.replace("\u2019", "'").split())
    bodies = {}
    for f in sorted(L.glob("ACD-1.[0-9].txt")):
        v = f.stem.split("-")[1]
        if tuple(map(int, v.split("."))) <= tuple(map(int, tv.split("."))):
            bodies[v] = norm(f.read_text(encoding="utf-8").split("-" * 80, 1)[-1])
    key = re.compile(r"\b(?:Dedicator|Dedication|the Work|Sections? \d)")
    mark = re.compile(r"(?:ACD-)?1\.[0-" + str(int(tv.split(".")[1]) - 1) + r"]\b|T\d+ の前|earlier version|formerly|used to|\bwas\b"
                      r"|no longer|corrected|replaced|旧|訂正|外し|外れ|だった|の前の形")
    faces = sorted({p for g in (*_OUTWARD470B, "ACD-OSI-BOTTLENECKS.md", "ADOPTING.md") for p in L.glob(g)})
    n, bad = 0, []
    # 段落の中で行をまたぐ引用も拾う (2026-11-27・d7・470b と同じ穴): 1 行ずつ見た版は 219 件、またいで拾うと 250 件。
    #   片の先頭 1 字の大小は区別しない —— 文頭の "So far as …" を文の途中で "so far as …" と引くのは引用の慣行で、
    #   区別すると QUESTIONS-FOR-COUNSEL の §6.2 が「1.1〜1.3 にだけ在る」と誤って出た (1.1〜1.3 は別の文の途中に小文字で在る)
    def _in(x, body):
        return x in body or (x[:1].swapcase() + x[1:]) in body
    for f in faces:
        text = f.read_text(encoding="utf-8")
        for m in re.finditer(r'\*"((?:(?!\n[ \t]*\n)[^"*]){12,}?)"\*', text):
            ln_no = text.count("\n", 0, m.start()) + 1
            q = norm(m.group(1))
            parts = [x.strip(" .,;:") for x in re.split(r"\.\.\.|…", q) if len(x.strip(" .,;:")) > 8]
            if not key.search(q) or not parts:
                continue
            n += 1
            if all(_in(x, bodies.get(tv, "")) for x in parts):
                continue
            older = [v for v in bodies if v != tv and all(_in(x, bodies[v]) for x in parts)]
            # 印を探す窓は、同じ段落の中の前 250 字・後 150 字 (旧版は「同じ行」で、折り返しの位置という偶然に依っていた。
            #   行で切ると QUESTIONS-FOR-COUNSEL §8 の *"whose infringement depends upon the use of the Work"* が、2 行前の
            #   "(in ACD-1.3)" を見ずに偽の RED になった)。段落 (空行) はまたがない
            win = text[max(0, m.start() - 250):m.end() + 150]
            a0 = m.start() - max(0, m.start() - 250)
            pa = max(win.rfind("\n\n", 0, a0), -1) + 1
            pb = win.find("\n\n", a0 + len(m.group(0)))
            if older and not mark.search(win[pa:pb if pb >= 0 else len(win)]):
                bad.append(f"{f.name}:{ln_no} ({'/'.join(older)}) *\"{q[:70]}\"*")
    check(bool(faces) and bool(bodies.get(tv)) and not bad,
          f"Check 470c: 外向きの文書の ACD の引用 {n} 件が、提出対象 ACD-{tv} の本文に在るか、前の版を名乗るか経緯の印を持つ",
          (f"Check 470c: 前の版にだけ在る文を、版を名乗らずに引いている {len(bad)} 件: {bad[:5]}。直し方は 2 つのどちらか: "
           f"(1) 引用を ACD-{tv} の本文の文に直す、(2) その引用のすぐ近く (同じ行) に版の名を 1 句添える —— 例 "
           "\"(in ACD-1.0)\"・\"ACD-1.3 said\"・「1.3 まで」。経緯の文なら「旧」「was」「no longer」などの印でもよい" if faces and bodies.get(tv) else
           f"Check 470c: 外向きの文書か ACD-{tv} の本文を読めない (黙って skip しない)"),
          blocking=True)


# 470b の対象: 審査者・法律家に出す、本文を「いまの文」として引く文書 (errata・against・試作の冊は途中の草案を歴史として引くので外す)
_OUTWARD470B = ("ACD-1.0.submission*.md", "REVIEWERS*.md", "ACD-1.*-CLAUSE-REFERENCE-DRAFT.md", "ACD-1.*.clause-reference.md", "FAQ*.md",
                "ACD-1.0.review-responses*.md", "ACD-1.0.objection-map.md", "SUBMISSION-MATERIALS.md", "READY-TO-SUBMIT.md",
                "QUESTIONS-FOR-COUNSEL.md")


def _selfquote_470b(ROOT, check):
    """470b の本体 (docstring の 470b)。返り値なし。"""
    L = ROOT / "LICENSES"
    norm = lambda s: re.sub(r"\s+", " ", s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')).strip()
    srcs = sorted(L.glob("ACD-1.*.txt")) + sorted(L.glob("CHANGES-ACD-*.txt"))
    low = " ".join(norm(p.read_text(encoding="utf-8")) for p in srcs).lower()
    words = re.findall(r"[a-z0-9']+", low)
    flat = " ".join(words)
    grams = {tuple(words[i:i + 3]) for i in range(len(words) - 2)}
    files = sorted({p for g in _OUTWARD470B for p in L.glob(g)})
    # 型ごとに 1 冊は当たること (2026-11-26・df): FAQ を改名したとき、古い型 "ACD-1.0.faq*.md" は何にも当たらず、FAQ が対象から黙って
    #   外れたまま 470b は緑だった (17 冊 → 16 冊)。改名・移動で型が空になったら止める
    empty = [g for g in _OUTWARD470B if not any(L.glob(g))]
    n, bad = 0, []
    for f in files:
        # 段落の中で行をまたぐ引用も拾う (2026-11-27・72 の報告・d7): 1 行ずつ見ていた版は、2 行にまたがる *"…"* を 1 片も見ず、
        #   REVIEWERS が "ACD-1.4 §1.7" として引いた確定前の草案の語 (#4273) と、QUESTIONS-FOR-COUNSEL の 1.3 と 1.4 草案を混ぜた引用を
        #   黙って通した (見える片 794 → 934)。空行はまたがない (別の段落の *" と "* を組にしない)
        text = f.read_text(encoding="utf-8")
        for m in re.finditer(r'\*"((?:(?!\n[ \t]*\n)[^"*]){12,600})"\*', text):
            line = text[max(0, m.start() - 40):m.end() + 40]
            ln_no = text.count("\n", 0, m.start()) + 1
            if re.search(r"\bT\d+\b", line):
                continue  # 試作の番号を添えた引用は途中の草案の歴史
            for part in (x.strip(" ,;") for x in re.split(r"\s*(?:…|\.\.\.)\s*", norm(m.group(1)).rstrip(".,;:"))):
                w = re.findall(r"[a-z0-9']+", part.lower())
                if len(w) < 4:
                    continue
                n += 1
                if part.lower() in low or " ".join(w) in flat:
                    continue
                g = [tuple(w[i:i + 3]) for i in range(len(w) - 2)]
                if sum(1 for x in g if x in grams) / len(g) >= 0.85:
                    bad.append(f"{f.name}:{ln_no} *\"{part[:90]}\"*")
    bad += [f"型 {g!r} に当たる文書が無い (改名・移動したなら _OUTWARD470B の型を直す)" for g in empty]
    check(bool(files) and not bad,
          f"Check 470b: 外向きの文書 {len(files)} 冊の本文の引用 {n} 片に、本文とほぼ同じで語のずれた引用は無い",
          (f"Check 470b: 本文とほぼ同じなのに、どの版の本文にも逐語で無い引用 {len(bad)} 件: {bad[:5]}。古い草案の文を"
           "「いまの文」として引いている形。凍結した版の逐語に直すか、途中の草案の歴史なら試作の番号 (T\\d+) を添える"
           if files else "Check 470b: 外向きの文書が 1 冊も見つからない (対象の glob を直す・黙って skip しない)"),
          blocking=True)

    # ── 505. 委員長でなかった時期の発言者を「委員長」と書かないこと (BLOCKING) ─────────
    from _lib_dossier import chair_term_misses
    _f505 = [f for f in sorted((ROOT / "LICENSES").glob("*.md"))] + sorted((ROOT / "docs" / "files" / "LICENSES").rglob("*.md"))
    _n505, _bad505 = chair_term_misses(_f505)
    check(
        not _bad505 and _n505 >= 25,
        f"Check 505: 委員長と書いた発言者 {_n505} 件が、在任の記録 (Nelson・Fontana・Chestek・Berkus・McCoy Smith) と合う",
        (f"Check 505: 発言の月の役と合わない「委員長」「元委員長」「のちの委員長」 {len(_bad505)} 件: {_bad505}。在任の表 (_lib_dossier.CHAIR_TERMS) の根拠に当てて直す"
         if _bad505 else f"Check 505: 拾えた文が {_n505} 件しか無い (25 件以上のはず。形か対象の glob が外れた)"),
        blocking=True,
    )
