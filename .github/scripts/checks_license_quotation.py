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
        _ls470 = _lic470.read_text(encoding="utf-8").split("\n")
        _st470 = []
        for _n470, _l470 in enumerate(_ls470):
            _m470 = re.match(r"^  (\d{1,2}\.\d{1,2})\s", _l470)
            if _m470:
                _st470.append((_m470.group(1), _n470))
        _clause470 = {}
        for _k470, (_c470, _n470) in enumerate(_st470):
            _e470 = _st470[_k470 + 1][1] if _k470 + 1 < len(_st470) else len(_ls470)
            _clause470[_c470] = _norm470("\n".join(_ls470[_n470:_e470]))

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
                _cov470 = set()
                for _r470 in _refs470:
                    _cov470.add(_r470)
                    if "." not in _r470:  # \u00a715 は \u00a715.2 を覆う
                        _cov470 |= {_k for _k in _clause470 if _k.startswith(_r470 + ".")}
                for _n470, _l470 in _blk470:
                    for _qm470 in _q470.finditer(_l470):
                        _quote470 = re.sub(r"\*\*|\\", "", next(_g for _g in _qm470.groups() if _g))
                        if len(_quote470.split()) < 5 or not re.search(r"[A-Za-z]{3}", _quote470):
                            continue
                        _nq470 = re.sub(r"[.,;:]+$", "", _norm470(_quote470)).strip()
                        _own470 = {_k for _k, _v in _clause470.items() if _nq470 in _v}
                        if not _own470:
                            continue  # \u30e9\u30a4\u30bb\u30f3\u30b9\u672c\u6587\u3067\u306a\u3044\u3082\u306e\u306f\u6bcd\u6570\u5916
                        _pop470 += 1
                        if not (_own470 & _cov470):
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
