#!/usr/bin/env python3
"""make_redline.py — ACD の 2 つの版の、条ごとの語の差 (redline) を 80 桁の plain text で出す。

**なぜ在るか (2026-11-15・50 の依頼)**: 審査者は新しいライセンスに「既存のものとの差」を求める ——
Chestek 氏 (2026-01-23) と Sado 氏 (2026-01-24) は redline か *"innovations only"* の抜粋を求めた
(`ACD-1.0.review-readings.md`)。計画の段 6b は、本申請の前に 1.4 の新しい語を 1.0 との差としてオーナーが
license-discuss へ出す。差を手で作ると、条の対応を取り違え (1.0 と 1.1 以降は条番号がずれる) 語を落とす。

**出すもの**: 新しい版の条の順に、条ごとに (a) 変わらない / (b) 変わった (語の差を `[-旧-]{+新+}` で) /
(c) 新設 / (d) 前の版にだけ在る、を出す。前文と節の見出しも同じ扱い。各行は 80 桁以内、ASCII のまま。
冒頭に 2 つの入力の file 名・sha256・語数を書く (どの本文の差かを読み手が確かめられるように)。

**条の対応**: 1.0 → 1.1 は条番号が並べ替えられた。対応は `LICENSES/ACD-1.1-CHANGELIST.md` §0.5 の表を読む
(確定版に当て直した表・単一の出所。この道具に写さない)。1.1 以降は条番号が同じ (草案の冒頭が
"Clause numbers follow ACD-1.3 (which follows ACD-1.1)" と述べる)。1.0 を旧にしたときは表を、
それ以外は同じ番号を当てる。表の行が読めなければ止まる (黙って同じ番号を当てない)。

**測っていないもの**: 法的効果。語の差は効果の差の証拠ではない。版番号と識別子の差も、そのまま差として出す。

使い方 (CI では回さない。出力は投稿の日・申請の日に作り、そのとき使った commit を書き添える):
    python3 .github/scripts/make_redline.py LICENSES/ACD-1.0.txt LICENSES/ACD-1.4-DRAFT.txt > redline.txt
    python3 .github/scripts/make_redline.py --changed-only LICENSES/ACD-1.3.txt LICENSES/ACD-1.4-DRAFT.txt
    python3 .github/scripts/make_redline.py --changed-only --context 8 LICENSES/ACD-1.0.txt LICENSES/ACD-1.4-DRAFT.txt
        # 変わった語の前後 8 語だけを残し、間を "..." にする (list に貼れる長さへ・2026-11-15。全文の redline は 1.0→1.4 で
        #   5,702 語あり、本体とほぼ同じ長さだった)
"""
from __future__ import annotations

import difflib
import hashlib
import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RULE = "-" * 80
CLAUSE = re.compile(r"^  (\d+\.\d+)\s+(.*?)(?=^  \d+\.\d+\s|^\d+\.\s|^END OF TERMS|\Z)", re.M | re.S)
HEAD = re.compile(r"^(\d+)\.\s+(\S.*)$", re.M)
MAP_TABLE = ROOT / "LICENSES" / "ACD-1.1-CHANGELIST.md"


def parts(text: str) -> dict[str, str]:
    """{key: 空白を正規化した本文}。key は "preamble" / "head N" / "N.M"。区切り線より上 (草案の注記) は読まない。"""
    body = text.split(RULE, 1)[1] if RULE in text else text
    end = body.find("END OF TERMS")
    body = body[:end] if end >= 0 else body
    out: dict[str, str] = {}
    pre = re.search(r"^PREAMBLE.*?$(.*?)(?=^1\.\s)", body, re.M | re.S)
    if pre:
        out["preamble"] = " ".join(pre.group(1).split())
    for m in HEAD.finditer(body):
        out[f"head {m.group(1)}"] = " ".join(m.group(2).split())
    for m in CLAUSE.finditer(body):
        out[m.group(1)] = " ".join(m.group(2).split())
    return out


def version_of(path: Path, text: str) -> str:
    m = re.search(r"Short identifier: ACD-(\d+\.\d+)", text)
    if not m:
        raise SystemExit(f"ERROR: {path} に Short identifier が無い")
    return m.group(1)


def map_from_10() -> dict[str, str | None]:
    """1.0 の条番号 → 1.1 以降の条番号 (削除は None)。表に無い番号は同じ番号。"""
    text = MAP_TABLE.read_text(encoding="utf-8")
    sec = text.split("## 0.5 ", 1)[1].split("\n## ", 1)[0] if "## 0.5 " in text else ""
    rows = [r for r in sec.split("\n") if r.startswith("|") and not r.startswith(("|---", "| 1.0 |"))]
    if not rows:
        raise SystemExit(f"ERROR: {MAP_TABLE.name} §0.5 の対応表を読めない (黙って同じ番号を当てない)")
    m: dict[str, str | None] = {}
    for r in rows:
        cells = [c.strip().strip("*").strip() for c in r.strip().strip("|").split("|")]
        old = re.findall(r"\d+\.\d+", cells[0])
        new = re.findall(r"\d+\.\d+", cells[1])
        if not old:
            continue  # 新設 (1.0 に無い)
        for o in old:
            m[o] = new[0] if new and len(old) == 1 else None
    return m


def wdiff(a: str, b: str, context: int | None = None) -> str:
    """語の差を [-旧-]{+新+} で。context を与えると、変わらない語の連なりは前後 context 語だけを残し、間を " ... " にする (出力は ASCII のまま)。"""
    aw, bw = a.split(), b.split()
    out = []
    ops = difflib.SequenceMatcher(a=aw, b=bw, autojunk=False).get_opcodes()
    for n, (op, i1, i2, j1, j2) in enumerate(ops):
        if op == "equal":
            run = aw[i1:i2]
            if context is not None and len(run) > 2 * context + 1:
                head = run[:context] if n > 0 else []
                tail = run[-context:] if n < len(ops) - 1 else []
                out.extend(head + ["..."] + tail)
            else:
                out.extend(run)
            continue
        if i2 > i1:
            out.append("[-" + " ".join(aw[i1:i2]) + "-]")
        if j2 > j1:
            out.append("{+" + " ".join(bw[j1:j2]) + "+}")
    return " ".join(out)


def fill(text: str, indent: str = "    ") -> str:
    return textwrap.fill(text, width=80, initial_indent=indent, subsequent_indent=indent,
                         break_long_words=False, break_on_hyphens=False)


def label(key: str) -> str:
    return {"preamble": "Preamble"}.get(key, f"Heading of Section {key[5:]}" if key.startswith("head ") else f"Section {key}")


def main(argv: list[str]) -> int:
    changed_only = "--changed-only" in argv
    context = int(argv[argv.index("--context") + 1]) if "--context" in argv else None
    args = [a for a in argv if not a.startswith("--") and not (context is not None and a == str(context))]
    if len(args) != 2 or "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0 if ("-h" in argv or "--help" in argv) else 2
    pa, pb = Path(args[0]), Path(args[1])
    ta, tb = pa.read_text(encoding="utf-8"), pb.read_text(encoding="utf-8")
    va, vb = version_of(pa, ta), version_of(pb, tb)
    A, B = parts(ta), parts(tb)
    m10 = map_from_10() if va == "1.0" and vb != "1.0" else {}
    to_new = {k: (m10.get(k, k) if re.fullmatch(r"\d+\.\d+", k) else k) for k in A}
    from_old = {v: k for k, v in to_new.items() if v}
    wa = len((ta.split(RULE, 1)[1] if RULE in ta else ta).split())
    wb = len((tb.split(RULE, 1)[1] if RULE in tb else tb).split())
    print(f"Redline: ACD-{va} -> ACD-{vb}, clause by clause, in the order of ACD-{vb}.")
    print(f"  Old: {pa.name}  sha256 {hashlib.sha256(ta.encode()).hexdigest()[:16]}  {wa} words")
    print(f"  New: {pb.name}  sha256 {hashlib.sha256(tb.encode()).hexdigest()[:16]}  {wb} words")
    print("  [-words-] are in the old text only; {+words+} are in the new text only.")
    if m10:
        print(f"  Clause numbers of ACD-1.0 are matched to ACD-{vb} by the table in")
        print("  LICENSES/ACD-1.1-CHANGELIST.md section 0.5; where a number moved, the")
        print("  old number is shown in brackets.")
    print("  Word differences are not differences of legal effect.")
    print()
    counts = {"unchanged": 0, "changed": 0, "new": 0, "removed": 0}  # new = 旧版に無い / removed = 新版に無い
    for key in B:
        old = from_old.get(key)
        tag = label(key) + (f" [ACD-{va} {old}]" if old and old != key else "")
        if old is None or old not in A:
            counts["new"] += 1
            # 番号の使い回し (2026-11-15・50 の検証): 1.0 の §15.5 / §15.6 は 1.1 で消え、1.2 / 1.3 が同じ番号に別の条を
            #   置いた。「new」とだけ書くと、旧版の同じ番号の条が消えて新しく出たのか取り違える
            reused = f" (ACD-{va} also has a Section {key}, with other content; see below)" if key in A else ""
            print(fill(f"{tag}: not in ACD-{va}{reused}", indent=""))
            print(fill("{+" + B[key] + "+}"))
            print()
        elif A[old] == B[key]:
            counts["unchanged"] += 1
            if not changed_only:
                print(f"{tag}: unchanged")
                print()
        else:
            counts["changed"] += 1
            print(f"{tag}: changed")
            print(fill(wdiff(A[old], B[key], context)))
            print()
    for key in A:
        if to_new.get(key) not in B:
            counts["removed"] += 1
            now = f" (ACD-{vb} uses the number {key} for other content)" if key in B else ""
            print(fill(f"{label(key)} of ACD-{va}: not in ACD-{vb}{now}", indent=""))
            print(fill("[-" + A[key] + "-]"))
            print()
    print("Summary: " + ", ".join(f"{v} {k}" for k, v in counts.items()) + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
