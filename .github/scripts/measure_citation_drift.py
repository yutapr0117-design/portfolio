#!/usr/bin/env python3
"""measure_citation_drift.py — 提出側の文書が引く条が、版をまたいで**意味を変えていないか**を測る。

**なぜ在るか。** Check 472 は「引いた条が提出対象の版に**存在するか**」を見る。
**存在するのに意味が違う場合を、それは捕まえられない。**
2026-09-19 の実測: 提出側 4 面が引く 1.0 の条 59 件のうち、**3 件が 1.2 に存在せず（472 が捕捉）**、
**18 件は番号が在るのに本文が変わっており、うち 7 件は一致度 0.15 未満**
（= **別の条になっている**）。とくに **§1 の定義は E13 の並べ替えで番号が入れ替わっており、
`§1.4`（"You" のつもり）は 1.2 では *Dedicator* を指す。**

**Check にしない理由**: 「意味が変わった」の閾値は判断であり、**正当な改訂（E4 で §6.4 の文言を
直した等）まで RED にする。** 道具として手で回し、**出た一覧を人が当たる。**
`measure_list_verbosity.py` / `measure_clause_clarity.py` と同じ位置づけ。

使い方:
    python3 .github/scripts/measure_citation_drift.py            # 1.0 → 現行草案
    python3 .github/scripts/measure_citation_drift.py 1.0 1.1    # 版を指定

条を引く行の一覧は `prepare_version_freeze.py --report` が `cited_lines()` を使って出す。
"""
from __future__ import annotations

import collections
import difflib
import pathlib
import re
import sys

from measure_quote_drift import FACES, _current_draft_version

ROOT = pathlib.Path(__file__).resolve().parents[2]
# 走査先と既定の版は導出する (measure_quote_drift.py と同じ外向きの定義)。4 面の決め打ちと既定「1.0 → 1.2」の
# 間は、想定問答と申請日の 1 枚が引く条を見ず、引数なしだと 2 版前の草案と比べていた (2026-11-04)。


CITE = re.compile(r"§\s?(\d{1,2}\.\d{1,2})|Sections?\s+(\d{1,2}\.\d{1,2})")
OTHER_CLAUSE = 0.15  # これ未満の一致度は、番号が同じでも別の条として扱う
# 申請の日に全部読む面。審査者と採用者が最初に読む。残りの外向きの面は、前の版と名指していない行だけ読む。
FIRST_READ = re.compile(r"(submission[^/]*|REVIEWERS|objection-map|SUBMISSION-MATERIALS|READY-TO-SUBMIT|ADOPTING)\.md$")


def _path(ver: str) -> pathlib.Path:
    p = ROOT / "LICENSES" / f"ACD-{ver}.txt"
    return p if p.exists() else ROOT / "LICENSES" / f"ACD-{ver}-DRAFT.txt"


def clauses(ver: str) -> dict[str, str]:
    """条番号 → 空白正規化した本文。冒頭の説明部は 80 本のダッシュで切る。"""
    t = _path(ver).read_text(encoding="utf-8")
    sep = "-" * 80
    lic = t.split(sep, 1)[1] if sep in t else t
    parts = re.split(r"\n  (?=(\d{1,2}\.\d{1,2})\s)", "\n" + lic)
    out: dict[str, str] = {}
    i = 1
    while i < len(parts):
        out[parts[i]] = " ".join(parts[i + 1].split())
        i += 2
    return out


def defined_term(body: str) -> str | None:
    m = re.search(r'"([^"]+)"\s+means', body)
    return m.group(1) if m else None


def _order(n: str) -> tuple[int, int]:
    return int(n.split(".")[0]), int(n.split(".")[1])


def moved(a_ver: str, b_ver: str) -> dict[str, str]:
    """a の条のうち、b で別の条になったものと、b に無いものを返す。"""
    a, b = clauses(a_ver), clauses(b_ver)
    kinds = {n: "無い条" for n in a if n not in b}
    kinds.update({n: "別の条" for n in a if n in b
                  and difflib.SequenceMatcher(None, a[n], b[n]).ratio() < OTHER_CLAUSE})
    return kinds


def cited_lines(a_ver: str, b_ver: str) -> tuple[dict[str, str], list[tuple[str, int, list[str], str]]]:
    """`moved` の番号を引く行を、外向きの面ごとに (面, 行番号, 番号, 本文) で返す。"""
    kinds = moved(a_ver, b_ver)
    rows = []
    for f in FACES:
        for i, line in enumerate((ROOT / "LICENSES" / f).read_text(encoding="utf-8").split("\n"), 1):
            hit = {m.group(1) or m.group(2) for m in CITE.finditer(line)} & set(kinds)
            if hit:
                rows.append((f, i, sorted(hit, key=_order), line))
    return kinds, rows


def main() -> int:
    a_ver, b_ver = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ("1.0", _current_draft_version())
    a, b = clauses(a_ver), clauses(b_ver)
    cited: dict[str, set[str]] = collections.defaultdict(set)
    for f in FACES:
        t = (ROOT / "LICENSES" / f).read_text(encoding="utf-8")
        for m in CITE.finditer(t):
            n = m.group(1) or m.group(2)
            if n in a:
                cited[n].add(f)

    gone, changed, same = [], [], []
    for n in sorted(cited, key=_order):
        if n not in b:
            gone.append(n)
            continue
        ratio = difflib.SequenceMatcher(None, a[n], b[n]).ratio()
        (same if ratio > 0.97 else changed).append((n, ratio))

    # 定義の写像は**語で**引く。番号で推測すると並べ替えの向きを間違える。
    terms_b = {defined_term(v): k for k, v in b.items() if defined_term(v)}
    remap = {n: terms_b.get(defined_term(a[n]))
             for n in a if n.startswith("1.") and defined_term(a[n])}

    print(f"外向きの {len(FACES)} 文書が引く ACD-{a_ver} の条: {len(cited)} 件")
    print(f"  🔴 ACD-{b_ver} に存在しない        : {gone or '無し'}   (Check 472 が BLOCKING で捕捉)")
    print(f"  🟡 番号は在るが本文が変わっている : {len(changed)} 件")
    for n, r in sorted(changed, key=lambda x: x[1]):
        mark = "  ← **別の条**" if r < OTHER_CLAUSE else ""
        print(f"       §{n:<5} 一致度 {r:.2f}{mark}   引用元 {sorted(cited[n])}")
    print(f"  🟢 実質同一                        : {len(same)} 件")
    print("\n定義の番号の写像 (語で照合):")
    for n in sorted(remap, key=lambda s: int(s.split(".")[1])):
        dst = remap[n] or "?"
        print(f"  {a_ver} §{n:<5} {defined_term(a[n]):<26} → {b_ver} §{dst}"
              + ("   ← 番号が動いた" if dst != n else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
