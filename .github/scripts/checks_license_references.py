"""
checks_license_references.py — ドシエが書いた矢印が、指した先に在るかを見る Check
(extracted from checks_license_dossier.py — check.py split track・category "reference resolution").

このモジュールが持つ invariant は 1 つ: **参照は解決する。**

**なぜ切り出したか。** 2026-09-15 に `checks_license_dossier.py` が advisory (800) を越えた。
**圧縮で誤魔化さず、いま触っているクラスタを切り出す**（house pattern）。

**この class の歴史を 1 行で**: 台帳は種類 7（相互参照）を **「機械強制済」と宣言していた**が、
**壊して測ると 7 形のうち 5 形が無防備だった**（`AUDIT-LEDGER.md` §7）。
**宣言と実測の差は、宣言した本人には見えない。**

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  471. **ドシエ内の参照記法が解決すること** (BLOCKING): Check 460 face (k) は `#N` と `E<n>`
       だけを見ていた。2026-09-14 の敵対的検証（主張の種類 7）で**参照記法を数え上げ、
       1 つずつ壊して測った**ところ、**7 形のうち 5 形が誰にも見られていなかった** ——
       `AUDIT-LEDGER.md` はこの種類を「機械強制済」と書いており、**その申告自身が誤りだった。**
       本 Check は**誤検出 0 を実測できた 3 形**を受け持つ: (a) `rounds/<file>` ——
       **「一次資料はここに在る」という証拠の主張そのもの**で、指した先が無ければ審査者は
       存在しない原文を探しに行く、(b) `B<n>` —— **方針を決めている register の項目** (286 箇所)、
       (c) `Check <N>` —— **実装の最大番号を超える参照は、存在しない機械強制を根拠として示す**
       ことになる (178 箇所)、(d) **`<file>.md` §N.M —— 文書を名指しした節参照** (実測 94 箇所)。
       (d) は 2026-09-15 に追加した —— **`review-corpus.md` §1.82 を 4 つの文書が引いていて、
       その節は存在しなかった**（参照を先に書いて本体を書かなかった）。**読み手は「そこに根拠が
       ある」と読んで探しに行く。** **残る 2 形は Check にしない**（裸の `` `file.md` `` 1,061 箇所と、
       **文書を名指ししない**裸の `§N.M` 2,024 箇所は、リポジトリ外・仮称・文脈依存を含み
       意味の判断が要る）。**ここに穴が残ることは台帳の種類 7 に書いてある。**

"""

import re


def run(ctx):
    """Run the reference-resolution Checks. ctx carries shared check()/ROOT by reference."""
    ROOT = ctx.ROOT
    check = ctx.check
    # ── 471. ドシエ内の参照記法が解決すること (BLOCKING) ──────────────────────────────────
    # **Check 460 face (k) は `#N` と `E<n>` だけを見ていた。** 2026-09-14 の敵対的検証
    # （主張の種類 7）で**ドシエの参照記法を数え上げ、1 つずつ壊して測った**ところ、
    # **7 形のうち 5 形が誰にも見られていなかった** —— 台帳はこの種類を「機械強制済」と
    # 書いており、**その申告自身が誤りだった。**
    #
    # 本 Check はそのうち**誤検出 0 を実測できた 3 形**を受け持つ:
    #   (a) `rounds/<file>` —— **ドシエの証拠の主張そのもの**（「一次資料は rounds/ に在る」）。
    #       指した先が無ければ、審査者は**存在しない原文を探しに行く**。
    #   (b) `B<n>` —— bottleneck register の項目 (286 箇所)。register は**方針を決めている
    #       文書**なので、番号が動いたときに黙って別の項目を指すのが最も高くつく。
    #   (c) `Check <N>` —— リポジトリの Check 番号 (178 箇所)。実装の最大番号を超える参照は、
    #       **存在しない機械強制を根拠として示している**ことになる。
    #
    # **残る 2 形は Check にしない**（意味の判断が要るため。#977 / #1212 と同じ）:
    # 裸の `` `file.md` `` (1,061 箇所・リポジトリ外や仮称も含む) と、
    # ドシエ内部の `§N.M` (2,024 箇所・どの文書の節かは文脈でしか決まらない)。
    # **ここに穴が残ることは `AUDIT-LEDGER.md` の種類 7 に書いてある。**
    _lic471 = ROOT / "LICENSES"
    _rounds471 = _lic471 / "rounds"
    if _rounds471.is_dir():
        _have471 = {_p.name for _p in _rounds471.iterdir() if _p.is_file()}
        _reg471 = _lic471 / "ACD-OSI-BOTTLENECKS.md"
        _ids471 = set()
        if _reg471.exists():
            _rt471 = _reg471.read_text(encoding="utf-8")
            _ids471 = (set(re.findall(r"\*\*(B\d{1,2})\*\*", _rt471))
                       | set(re.findall(r"^\| (B\d{1,2}) \|", _rt471, re.M)))
        # 最大 Check 番号は**実装から導出する**（決め打ちは Check を足すたび stale になる）。
        _max471 = 0
        _scripts471 = ROOT / ".github" / "scripts"
        for _cf471 in sorted(_scripts471.glob("checks_*.py")) + [_scripts471 / "check_repository_consistency.py"]:
            if _cf471.exists():
                for _m471 in re.finditer(r"# \u2500\u2500 (\d{1,3})[a-z]?\.", _cf471.read_text(encoding="utf-8")):
                    _max471 = max(_max471, int(_m471.group(1)))

        def _expand471(_s):
            # `rounds/…-{discuss,review}-…txt` のような brace 記法を展開する。
            # **展開せずに数えると、正しい参照を「解決しない」と報告する**（実測 1 件）。
            _m = re.search(r"\{([^}]*)\}", _s)
            if not _m:
                return [_s]
            return [_x for _alt in _m.group(1).split(",")
                    for _x in _expand471(_s[:_m.start()] + _alt + _s[_m.end():])]

        # 各ドシエ file が実際に持つ節 id（見出しの先頭の番号 / 英字ラベル）
        _heads471 = {}
        for _hf471 in sorted(_lic471.glob("*.md")) + sorted(_rounds471.glob("*.md")):
            _ids471h = set()
            for _hl471 in _hf471.read_text(encoding="utf-8").split("\n"):
                _mh471 = re.match(r"^#{1,6}\s+([0-9]+(?:\.[0-9]+)*[a-z]?)\b", _hl471)
                if _mh471:
                    _ids471h.add(_mh471.group(1))
                _mh471b = re.match(r"^#{1,6}\s+\u00a7?\s*([A-Z](?:\.[0-9]+)*)\b", _hl471)
                if _mh471b:
                    _ids471h.add(_mh471b.group(1))
            _heads471[_hf471.name] = _ids471h

        # 各 file の見出し番号（`## 1.49 …` / `### B.0 …` / `#### 1.70b …`）
        _head471re = re.compile(
            r"^#{1,6}\s+\**\s*\u00a7?\s*([0-9]+(?:\.[0-9]+)*[a-z]?|[A-Z](?:\.[0-9]+)*[a-z]?)[ .\uff0e\u3000]")
        _headnum471 = {}
        for _hf471 in sorted(_lic471.glob("*.md")):
            _s471 = set()
            for _hl471 in _hf471.read_text(encoding="utf-8").split("\n"):
                _mh471 = _head471re.match(_hl471)
                if _mh471:
                    _s471.add(_mh471.group(1))
            _headnum471[_hf471.name] = _s471
        _allnum471 = set().union(*_headnum471.values()) if _headnum471 else set()
        # ライセンス条項 id（凍結本文から導出）
        _clause471 = set()
        _txt471 = _lic471 / "ACD-1.0.txt"
        if _txt471.exists():
            for _cl471 in _txt471.read_text(encoding="utf-8").split("\n"):
                _mc471 = re.match(r"^  (\d{1,2}\.\d{1,2})\s", _cl471)
                if _mc471:
                    _clause471.add(_mc471.group(1))
                _mc471b = re.match(r"(\d{1,2})\.\s+[A-Z]", _cl471)
                if _mc471b:
                    _clause471.add(_mc471b.group(1))
        # 想定問答の Q 番号（`\u00a731` / `\u00a732` はこの Q を指す記法として使われている）
        _qnum471 = set()
        for _qf471 in sorted(_lic471.glob("ACD-1.0.review-responses*.md")):
            _qnum471 |= set(re.findall(r"^#{1,6}\s+Q(\d+)[a-z]?\.",
                                       _qf471.read_text(encoding="utf-8"), re.M))
        _bare471 = re.compile(
            r"\u00a7\s?([0-9]+(?:\.[0-9]+)*[a-z]?|[A-Z](?:\.[0-9]+)*[a-z]?)(?![0-9a-zA-Z.])")
        _named471 = re.compile(r"`[A-Za-z0-9._\-]+\.md`\s*(?:\u306e)?\s*$")

        _bad471 = []
        _files471 = sorted(_lic471.glob("*.md")) + sorted((ROOT / "docs" / "files" / "LICENSES").glob("*.md"))
        for _f471 in _files471:
            for _i471, _l471 in enumerate(_f471.read_text(encoding="utf-8").split("\n"), 1):
                # (a) rounds/ —— 拡張子で終端を決める。**行の折り返しや省略記号 (…) を
                # 終端と見なすと、正しい参照を誤検出する**（実測 2 件）。
                for _m471 in re.finditer(r"rounds/([0-9][A-Za-z0-9._\-{},]+\.(?:txt|md))", _l471):
                    for _cand471 in _expand471(_m471.group(1)):
                        if _cand471 not in _have471:
                            _bad471.append(f"{_f471.name}:{_i471} `rounds/{_cand471}` が実在しない")
                # (b) B<n>
                if _ids471:
                    for _m471 in re.finditer(r"(?<![A-Za-z0-9])B(\d{1,2})(?![0-9A-Za-z])", _l471):
                        if "B" + _m471.group(1) not in _ids471:
                            _bad471.append(f"{_f471.name}:{_i471} `B{_m471.group(1)}` が register の項目に解決しない")
                # (d) `<file>.md` §N.M —— **文書を名指しした節参照。** 2026-09-15 に実測したところ
                # **`review-corpus.md` §1.82 を 4 つの文書が引いていて、その節は存在しなかった**
                # （参照を先に書いて本体を書かなかった）。**読み手は「そこに根拠がある」と読んで
                # 探しに行く。** ドシエ内部の裸の `§N.M`（どの文書の節かが文脈でしか決まらない）は
                # 依然 Check にしないが、**文書を名指しした形は曖昧さが無い**（実測 94 件・誤検出 0）。
                for _m471 in re.finditer(
                        r"`([A-Za-z0-9._\-]+\.md)`\s*(?:\u306e)?\s*\u00a7\s*"
                        r"([0-9]+(?:\.[0-9]+)*[a-z]?|[A-Z](?:\.[0-9]+)*)", _l471):
                    _tgt471, _sec471 = _m471.group(1), _m471.group(2)
                    if _tgt471 in _heads471 and _sec471 not in _heads471[_tgt471]:
                        _bad471.append(
                            f"{_f471.name}:{_i471} `{_tgt471}` \u00a7{_sec471} \u304c\u5b9f\u5728\u3057\u306a\u3044")
                # (e) **裸の `§N.M`** —— 文書を名指ししない節参照 (実測 3,190 箇所)。
                # **2026-09-14 には「文脈でしか決まらないので Check にしない」と書いた。
                # その判断は、記法を 1 つの形として見ていたから出た。** 実際には
                # **解決先を列挙できる**: ライセンス条項 / その file 自身の節 / 提出パケットの
                # §1b・§4c 等 / **4 file に分かれた §1.xx の共有採番**（comparison・
                # review-precedents・review-corpus・reviewer-positions）。**列挙すると残りは 18 箇所**で、
                # **そのうち 17 は正当**（`§X` `§N` の placeholder / `§1.4x` の wildcard /
                # 外国法の条番号 `§365` `§309` / 想定問答の `§31` `§32` = Q 記法）。
                # **残る 1 箇所が実欠陥だった** —— どこにも存在しない `§27` を「失敗」として引いていた。
                # **一般形: 「機械で判定できない」と結論する前に、その形が単一の形かを見る。**
                _series471 = set()
                for _sf471 in ("ACD-1.0.comparison.md", "ACD-1.0.review-precedents.md",
                               "ACD-1.0.review-corpus.md", "ACD-1.0.reviewer-positions.md"):
                    _series471 |= _headnum471.get(_sf471, set())
                _pack471 = (_headnum471.get("ACD-1.0.submission.md", set())
                            | _headnum471.get("ACD-1.0.submission-reference.md", set()))
                for _m471 in _bare471.finditer(_l471):
                    _sid471 = _m471.group(1)
                    if _named471.search(_l471[:_m471.start()]):
                        continue                                  # face (d) の射程
                    if re.fullmatch(r"[A-Za-z]|\d+\.\d*[a-z]", _sid471):
                        continue                                  # placeholder / wildcard
                    if re.fullmatch(r"\d{3,}", _sid471):
                        continue                                  # 外国法の条番号
                    # 想定問答の Q 記法（`\u00a731` = Q31）。**行が想定問答を名指ししているときだけ**認める ——
                    # **無条件に認めると、Q27 が在るせいで実欠陥の `\u00a727` が黙って解決してしまう**
                    # （初版で実際にそうなり、動機となった欠陥を gate が素通しした）。
                    if _sid471 in _qnum471 and (
                            re.search(r"\u60f3\u5b9a\u554f\u7b54|\u5206\u518a|review-responses", _l471)
                            or "review-responses" in _f471.name):
                        continue
                    if (_sid471 in _clause471 or _sid471 in _headnum471.get(_f471.name, set())
                            or _sid471 in _pack471 or _sid471 in _series471
                            or _sid471 in _allnum471):
                        continue
                    _bad471.append(f"{_f471.name}:{_i471} `\u00a7{_sid471}` \u306f\u3069\u306e\u6587\u66f8\u306e\u7bc0\u306b\u3082\u89e3\u6c7a\u3057\u306a\u3044")
                # (c) Check <N>
                if _max471:
                    for _m471 in re.finditer(r"Check (\d{1,4})", _l471):
                        if int(_m471.group(1)) > _max471:
                            _bad471.append(f"{_f471.name}:{_i471} `Check {_m471.group(1)}` は実装の最大番号 {_max471} を超える")
        check(
            not _bad471,
            f"Check 471: \u30c9\u30b7\u30a8\u306e\u53c2\u7167\u8a18\u6cd5 4 \u5f62 (rounds/ \u30d1\u30b9 / B<n> / Check N / \u540d\u6307\u3057\u3057\u305f \u00a7N.M) \u304c\u3059\u3079\u3066\u89e3\u6c7a\u3059\u308b",
            (f"Check 471: \u30c9\u30b7\u30a8\u5185\u306e\u53c2\u7167\u304c\u89e3\u6c7a\u3057\u306a\u3044: {_bad471}\u3002"
             "**`rounds/` \u306f\u300c\u4e00\u6b21\u8cc7\u6599\u306f\u3053\u3053\u306b\u5728\u308b\u300d\u3068\u3044\u3046\u8a3c\u62e0\u306e\u4e3b\u5f35\u305d\u306e\u3082\u306e**\u3067\u3042\u308a\u3001"
             "**`B<n>` \u306f\u65b9\u91dd\u3092\u6c7a\u3081\u3066\u3044\u308b register \u306e\u9805\u76ee**\u3067\u3042\u308a\u3001"
             "**`Check <N>` \u306f\u5b58\u5728\u3057\u306a\u3044\u6a5f\u68b0\u5f37\u5236\u3092\u6839\u62e0\u3068\u3057\u3066\u793a\u3059\u3053\u3068\u306b\u306a\u308b**\u3002"
             "\u53c2\u7167\u5148\u3092\u76f4\u3059\u304b\u3001\u53c2\u7167\u3092\u3084\u3081\u3066\u8a18\u8ff0\u306b\u305b\u3088"),
            blocking=True,
        )
