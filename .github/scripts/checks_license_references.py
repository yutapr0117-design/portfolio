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
  471. **ドシエが書いた矢印が、指した先に在ること** (BLOCKING・6 形): Check 460 face (k) は `#N` と `E<n>`
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
       **(i)・2026-09-25**: 英語で書いた英字節参照 `section B.2` —— face (e) は `§` 付きしか見ず、
       SPDX 提出文が存在しない「section B.2 above」を指していたのを素通りした。
       **(h)・2026-09-24**: 他文書を行番号（`` `file.md` L123 ``）で指さないこと —— 行番号は書いた日の
       位置でしかなく、確定手順の表が 11 箇所中 9 箇所で既に別の行を指していた。

"""

import re

# **`Check <N>` 参照の単一の読み取り口**（face (c) と face (g) が共有する）。
# **並びの 2 番目以降まで取るのが要点** ——先頭だけ見る実装は、この repo で
# 最も普通の書き方（`Check 45 / 70 / 105`）の大半を検証しない。
_CHECKREF471 = re.compile(r"\bChecks?\s+(\d{1,4})((?:\s*[/,、・]\s*\d{1,4})+)?")


def _checknums471(m):
    """マッチから、先頭と並びの残り全部の番号を返す."""
    nums = [int(m.group(1))]
    if m.group(2):
        nums += [int(x) for x in re.findall(r"\d{1,4}", m.group(2))]
    return nums


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
                # **2026-09-24: 決め打ちの 5 file から導出へ。** face (f) は 09-19 に導出へ直したが
                # この (e) は残っていた ——**同じ系列を見る 2 つの face が別の file 集合を見ていた。**
                # 分割で生まれた `review-venue.md` の節を指す裸の参照が、ここだけで未解決になる。
                for _sf471 in sorted(_p.name for _p in _lic471.glob("ACD-1.0.*.md")):
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
                # (i) **英語で書いた英字節参照 `section B.2`**（2026-09-25）。face (e) は `\u00a7` で
                # 始まる形しか見ておらず、**SPDX 提出文 §C が「section B.2 above」と存在しない節を
                # 指していたのを素通りした**（比較は分割時に `submission-reference.md` §2 へ移っていた）。
                # 英字の節（A.0 / B.0 / E.1 …）は提出パケットにしか無いので、解決先はその 2 file の見出し。
                # **数字の `Section 8.4` はライセンス条項を指すので対象外**（英字 1 文字で始まる形だけを見る）。
                for _m471 in re.finditer(r"\b[Ss]ection\s+([A-Z]\.[0-9]+[a-z]?)\b", _l471):
                    if _m471.group(1) not in _pack471:
                        _bad471.append(
                            f"{_f471.name}:{_i471} `section {_m471.group(1)}` \u306f\u63d0\u51fa\u30d1\u30b1\u30c3\u30c8\u306e\u7bc0\u306b\u89e3\u6c7a\u3057\u306a\u3044")
                # (c) Check <N> / Checks <N> / 番号の並び
                # ⚠ **2026-09-22 に 3 つの穴を実測で塞いだ**（別記法で殴って RED を確かめる掃引）:
                #   (1) **複数形 `Checks N`** ——素通りしていた。実使用 3 箇所で、**うち 1 つは
                #       入口ページ `REVIEWERS.md` の「Checks 444, 460」**である。
                #   (2) **並びの 2 番目以降** ——スラッシュ・カンマ・読点で番号を並べた形は、
                #       **先頭しか検証されていなかった**（2 番目以降が存在しない番号でも緑）。
                #       この書き方は規範層で 322 + 29 + 141 箇所使われている。
                #   (3) 走査範囲は face (g) で広げた（下）。
                if _max471:
                    for _m471 in _CHECKREF471.finditer(_l471):
                        for _n471 in _checknums471(_m471):
                            if _n471 > _max471:
                                _bad471.append(
                                    f"{_f471.name}:{_i471} `Check {_n471}` は実装の最大番号 {_max471} を超える")
        # (g) **走査範囲を規範層へ広げる（2026-09-22）。**
        # face (c) は `LICENSES/` しか見ておらず、**該当参照 約 3,454 件のうち 235 件
        # （6.8%）しか検証していなかった。** だが face (c) が名指しする害 ——
        # **「存在しない機械強制を根拠として示す」** —— が最も起きやすいのは
        # **規範層（check-map / runbook / CLAUDE.md / mirror）**で、そこに 1,654 + 308 + 755 件が在る。
        # ⚠ **広げる前に誤検出を測った: 3,454 件すべてが最大番号以下で、RED は 0 件。**
        # ⚠ **`docs/incident-artifacts/` と `docs/session-records/` は対象外** ——
        # 分割前に書かれた歴史記録であり、書き換えれば履歴を偽る
        # (`check-repository-consistency-map.md` §2.9 / §2.10 と同じ線引き)。
        if _max471:
            _scope471g = sorted(
                list((ROOT / "docs" / "architecture").glob("*.md"))
                + [ROOT / "CLAUDE.md", ROOT / ".claude" / "CLAUDE.md"]
                + [_q for _q in (ROOT / "docs" / "files").rglob("*.md")
                   if "incident-artifacts" not in _q.parts and "session-records" not in _q.parts])
            for _q471g in _scope471g:
                if not _q471g.exists():
                    continue
                for _i471g, _l471g in enumerate(_q471g.read_text(encoding="utf-8").splitlines(), 1):
                    for _m471g in _CHECKREF471.finditer(_l471g):
                        for _n471g in _checknums471(_m471g):
                            if _n471g > _max471:
                                _bad471.append(
                                    f"{_q471g.name}:{_i471g} `Check {_n471g}` は実装の最大番号 "
                                    f"{_max471} を超える (規範層 —— 存在しない機械強制を根拠にしている)")

        # (f) **`\u00a71.xx` の共有採番が衝突しないこと。** この採番は 4 file に分かれており
        # （comparison / review-precedents / review-corpus / reviewer-positions）、
        # **同じ番号を 2 つの file が使うと、参照は「解決する」のに別の節へ着く。**
        # **Check 471 (d)(e) は解決性しか見ないので、この形は原理的に捕捉できない。**
        # 2026-09-15 に実害: **`\u00a71.82` は既に在ったのに、見出しを `###` で grep して
        # 見落とし、「4 文書が引く節が存在しない」と誤診して新しい `\u00a71.82` を書いた。**
        # **診断が誤りで、その「修正」が本物の重複を作った。**
        # **既存の 3 件（1.67 / 1.68 / 1.69）は grandfather する** ——番号を動かすと
        # 既存の参照がどちらを指すか決められなくなる（本 file 群の規約は「節番号を動かさない」）。
        _grand471 = {"1.67", "1.68", "1.69"}
        # **⚠ 2026-09-19: 決め打ちの 5 file から導出へ変えた。** 決め打ちは書いた日の正しさしか
        # 持たず、**実測すると `dig-2026-09.md`(4) / `objection-map.md`(1) の 2 file が最初から
        # 射程外**で、同日の分割で生まれた `review-labels.md`(2) も**静かに射程外になった**
        # ——**衝突を見張る Check が、見張る対象の一部を見ていなかった**（Check 124 / 411 /
        # 435b と同じ scope-drift の族）。**共有採番が住むのは `ACD-1.0.*.md` である**ことを
        # 単一の根拠にして導出する（`REVISION-PROTOCOL.md` の §1.5 は**その文書自身の節番号**で
        # 共有系列ではないため、prefix で自然に外れる）。
        _seriesfiles471 = tuple(sorted(_p471.name for _p471 in _lic471.glob("ACD-1.0.*.md")))
        _own471 = re.compile(r"^#{1,6}\s+\**\s*(1\.\d+[a-z]?)[ .\uff0e\u3000]")
        _where471 = {}
        for _sf471 in _seriesfiles471:
            _sp471 = _lic471 / _sf471
            if not _sp471.exists():
                continue
            for _sl471 in _sp471.read_text(encoding="utf-8").split("\n"):
                _ms471 = _own471.match(_sl471)
                if _ms471:
                    _where471.setdefault(_ms471.group(1), []).append(_sf471)
        for _sid471, _fs471 in sorted(_where471.items()):
            if len(_fs471) > 1 and _sid471 not in _grand471:
                _bad471.append(
                    f"\u00a7{_sid471} \u304c\u8907\u6570\u306e file \u306b\u5b58\u5728\u3059\u308b: {_fs471} "
                    f"\uff08\u53c2\u7167\u306f\u89e3\u6c7a\u3059\u308b\u304c\u5225\u306e\u7bc0\u3078\u7740\u304f\uff09")

        # (h) **他文書を行番号 (`L123`) で指さないこと。** 行番号は書いた日の位置であって、
        # 読む日の位置ではない。2026-09-24 に `ACD-1.2-CHANGELIST.md` の確定手順の表が
        # `submission-reference.md` を 11 箇所行番号で指しており、**9 箇所が既に別の行を指していた**
        # （確定の日に表どおり置換すると別の文を書き換える）。件数か導出コマンドで書く。
        _lnref471 = re.compile(r"`[\w./-]+\.(?:md|txt|py)`[^|\n]{0,8}\bL\d{2,4}\b")
        for _lf471 in sorted(_lic471.glob("*.md")):
            for _li471, _ll471 in enumerate(_lf471.read_text(encoding="utf-8").split("\n"), 1):
                if _lnref471.search(_ll471):
                    _bad471.append(f"{_lf471.name}:{_li471} \u884c\u756a\u53f7\u3067\u4ed6\u6587\u66f8\u3092\u6307\u3057\u3066\u3044\u308b (face h)")

        check(
            not _bad471,
            f"Check 471: \u30c9\u30b7\u30a8\u306e\u53c2\u7167\u8a18\u6cd5 8 \u5f62 (rounds/ \u30d1\u30b9 / B<n> / Check N / \u540d\u6307\u3057\u306e \u00a7N.M / \u88f8\u306e \u00a7N.M / section B.0 / \u5171\u6709\u63a1\u756a\u306e\u4e00\u610f\u6027 / \u884c\u756a\u53f7\u53c2\u7167\u306e\u4e0d\u5728) \u304c\u3059\u3079\u3066\u89e3\u6c7a\u3059\u308b",
            (f"Check 471: \u30c9\u30b7\u30a8\u5185\u306e\u53c2\u7167\u304c\u89e3\u6c7a\u3057\u306a\u3044: {_bad471}\u3002"
             "**`rounds/` \u306f\u300c\u4e00\u6b21\u8cc7\u6599\u306f\u3053\u3053\u306b\u5728\u308b\u300d\u3068\u3044\u3046\u8a3c\u62e0\u306e\u4e3b\u5f35\u305d\u306e\u3082\u306e**\u3067\u3042\u308a\u3001"
             "**`B<n>` \u306f\u65b9\u91dd\u3092\u6c7a\u3081\u3066\u3044\u308b register \u306e\u9805\u76ee**\u3067\u3042\u308a\u3001"
             "**`Check <N>` \u306f\u5b58\u5728\u3057\u306a\u3044\u6a5f\u68b0\u5f37\u5236\u3092\u6839\u62e0\u3068\u3057\u3066\u793a\u3059\u3053\u3068\u306b\u306a\u308b**\u3002"
             "\u53c2\u7167\u5148\u3092\u76f4\u3059\u304b\u3001\u53c2\u7167\u3092\u3084\u3081\u3066\u8a18\u8ff0\u306b\u305b\u3088"),
            blocking=True,
        )
