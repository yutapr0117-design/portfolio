"""_lib_draft_faces.py — Check 468 の面のうち、本体の長いもの (468y・468z) を置く。

**なぜ在るか (2026-11-23・fc)**: `checks_license_draft.py` が 933 行で Check 52 の advisory (900) を越え、BLOCKING の 1,000 行
(Check 365) に近づいた。Check 468 は 1 つの `# ── 468.` 区間なので面を module 間で分けられず、面の本体を helper へ移す
(2026-11-15 に 468n・468s を `_lib_draft_counts.py` へ移したのと同じ手)。区間・ラベル・OK 行は `checks_license_draft.py` に残る。
本体は移す前と同じ (変数の名だけを引数に替えた)。
"""
from __future__ import annotations

import re
from pathlib import Path


def faces_468yz(ROOT: Path, dr: Path, cl: set, t468: str) -> tuple[list[str], int, "int | None", set]:
    """468y と 468z。返り値: (誤りの文, 468y の組の数, 468z の参照の数 (節が無ければ None), 468z の異なる条)。"""
    bad: list[str] = []
    # ── 468y: 試作で「変えない」「退けた」とした条の、逐条の下書きの行がその試作に触れていること ─────────
    #   portfolio-aa の依頼 (2026-11-11)。見出しが「変えない」「退けた」を述べる試作の節について、見出しの §N.M と、
    #   節の中の「変えない理由」の列を持つ表の 1 列目の §N.M を扱った条とし、逐条の下書きのその条の行が、見出しの
    #   T 番号か節の番号 (§14.N) を含むこと。審査者は逐条の行で条を読むので、試作の結論 (変えない理由) が
    #   そこから辿れないと、同じ問いを同じ答えのまま繰り返させる。いままで手で揃えていた (6 組)
    _v468y = dr.name.split("-")[1]
    # 試作は 2 冊目から 3 冊目へ続く (2026-11-15: 2 冊目が 1,000 行に当たり §15 から THIRD へ分けた)。作業中の版の試作の
    #   冊をすべて読む (2026-11-23・fc: 1.4 の確定の後、名で決め打ちした SECOND / THIRD は 1.5 に無く、1.5 の試作
    #   ACD-1.5-CLARITY-TRIAL.md を 1 つも読まずに黙っていた)
    _trs468y = sorted((ROOT / "LICENSES").glob(f"ACD-{_v468y}-*CLARITY-TRIAL.md"))
    _tr468y = _trs468y[0] if _trs468y else ROOT / "LICENSES" / f"ACD-{_v468y}-CLARITY-TRIAL.md"
    # 逐条の下書きは作業中の版のものが無ければ、直前の版のもの (次版の逐条は確定まで書き直さない・1.4 の逐条が 1.5 の条を述べる)
    # 逐条は確定の後に ACD-N.M.clause-reference.md へ改名しうる (2026-11-23 の合議の小議題)。新旧どちらの名も読む
    _crs468y = sorted([*(ROOT / "LICENSES").glob("ACD-1.*-CLAUSE-REFERENCE-DRAFT.md"), *(ROOT / "LICENSES").glob("ACD-1.*.clause-reference.md")],
                      key=lambda _p: int(re.match(r"ACD-1\.(\d+)", _p.name).group(1)))
    _cr468y = ROOT / "LICENSES" / f"ACD-{_v468y}-CLAUSE-REFERENCE-DRAFT.md"
    if not _cr468y.exists() and _crs468y:
        _cr468y = _crs468y[-1]
    _pairs468y, _miss468y = 0, []
    if _tr468y.exists():
        _trt = "\n".join(_p.read_text(encoding="utf-8") for _p in _trs468y if _p.exists())
        _rows468y = {}
        for _l in (_cr468y.read_text(encoding="utf-8").split("\n") if _cr468y.exists() else []):
            _mr = re.match(r"^\|\s*\*\*(\d+\.\d+)\*\*\s*\|", _l)
            if _mr:
                _rows468y[_mr.group(1)] = _l
        # 見出しは 1.4 の冊が「### 14.25 …」、1.5 の冊が「## 1. T135 —— …」の形 (2026-11-23)。両方を節として読む
        _secs = list(re.finditer(r"^#{2,3} (\d+(?:\.\d+)?)\.? (.*)$", _trt, re.M))
        for _k, _ms in enumerate(_secs):
            if not re.search(r"変えない|退けた", _ms.group(2)):
                continue
            _body = _trt[_ms.end():_secs[_k + 1].start() if _k + 1 < len(_secs) else len(_trt)]
            _cls = set(re.findall(r"§(\d+\.\d+)", _ms.group(2)))
            for _tm in re.finditer(r"^\|[^\n]*変えない理由[^\n]*\|\n\|[-: |]+\|\n((?:\|[^\n]*\n)+)", _body, re.M):
                for _r in _tm.group(1).splitlines():
                    _cls |= set(re.findall(r"§(\d+\.\d+)", _r.split("|")[1]))
            _refs = sorted(set(re.findall(r"\bT\d+\b", _ms.group(2)))) + ["§" + _ms.group(1)]
            for _c in sorted(_cls):
                _pairs468y += 1
                if not any(re.search(re.escape(_x) + r"(?!\d)", _rows468y.get(_c, "")) for _x in _refs):
                    _miss468y.append(f"§{_c} ← {'/'.join(_refs)}")
        if not _cr468y.exists() and _pairs468y:
            bad.append(f"468y: {_tr468y.name} は在るのに {_cr468y.name} が無い")
        elif _miss468y:
            bad.append(f"468y: 試作で変えない / 退けたとした条の逐条の行が、その試作に触れていない: {_miss468y}。"
                           "行に T 番号か節の番号 (§N.M) を書き、結論 (変えない理由) を辿れるようにする")

    # ── 468z: CHANGELIST の「記述子の下書き」の表が引く §N.M と note の "Section N.M" が、草案に実在すること ─────
    #   aa の問い (2026-11-11): 凍結版の記述子の note は 451f が照合するが、確定の日まで記述子は CHANGELIST の表の中の下書きで
    #   照合の外だった。条の番号は試作で動くので、下書きの番号が草案に無くなったら確定の日を待たずに RED にする
    _cltxt468z = dr.with_name(dr.name.replace("-DRAFT.txt", "-CHANGELIST.md"))
    # 1.5 からは「## 記述子の候補」の節に箇条で書く (2026-11-23・確定の道具の雛形)。旧い「### N.M の記述子の下書き」の表も読む。
    #   節の名が変わっただけで 468z は OK 行に「—」を出して黙っていた (1.5 の候補 §5.2 を照らしていなかった)
    _ms468z = re.search(r"^(?:### " + re.escape(_v468y) + r" の記述子の下書き|## 記述子の候補).*?(?=^#{1,3} |\Z)",
                        _cltxt468z.read_text(encoding="utf-8") if _cltxt468z.exists() else "", re.S | re.M)
    _n468z, _u468z = None, set()   # 下書きの節が無い版では OK 行に「—」と出す (黙って 0 と書かない)
    if _ms468z:
        _secs468z = {_n.split(".", 1)[0] for _n in cl}
        _miss468z, _n468z = [], 0
        for _l in (_x for _x in _ms468z.group(0).split("\n") if _x.startswith(("|", "- "))):
            _cs = [_c for _m in re.finditer(r"\b[Ss]ections?\s+(\d+(?:\.\d+)?(?:(?:,\s*|\s+and\s+|\s+or\s+|\s+to\s+)"
                                              r"\d+(?:\.\d+)?)*)", _l) for _c in re.findall(r"\d+(?:\.\d+)?", _m.group(1))]
            _cs += re.findall(r"§(\d+\.\d+)", _l)
            for _c in _cs:
                _n468z += 1
                _u468z.add(_c)
                if _c not in (cl if "." in _c else _secs468z):
                    _miss468z.append(_c)
        # 表の逐語 (*"…"*) も草案に在る (11-12・aa: T22 より前の語が残っていた)。記述子自身の文 (note / $comment) と旧い文は除く
            # 本文 (区切り線の後) だけで照らす (2026-11-23): t468 は冒頭の変更の一覧も含み、一覧が逐語を引けば本文から消えても通る
        #   (468x で実測した形・#3970)
        _d468z = " ".join(t468.split("-" * 80, 1)[-1].split())
        for _mq in re.finditer(r'\*"(.+?)"\*', "\n".join(_x for _x in _ms468z.group(0).split("\n") if _x.startswith(("|", "- ")))):
            _q = " ".join(_mq.group(1).replace('\\"', '"').split()).strip(" .,;:")
            if not re.search(r"note|\$comment|より前の|旧|訂正前", _mq.string[max(0, _mq.start() - 40):_mq.start()]) and not all(
                    _p.strip(" .,;:") in _d468z for _p in re.split(r"…|\.\.\.", _q) if len(_p.strip()) > 3):
                _miss468z.append(f"逐語 {_q[:50]!r}")
        if _miss468z:
            bad.append(f"468z: {_cltxt468z.name} の記述子の下書きが、草案に無い条か語を引く: {sorted(set(_miss468z))}")
        elif not _n468z:
            bad.append(f"468z: {_cltxt468z.name} の記述子の下書きから条の参照を 1 件も読めない (読めないまま黙らせない)")

    return bad, _pairs468y, _n468z, _u468z
