#!/usr/bin/env python3
"""moved_clauses.py — 判定した後に動いた条を出す（台帳の行が、いまの本文についての判定のままかを見る）。

**なぜ在るか (2026-11-24・3f の依頼)**: 1.5 の書き直しは 1 日に 37 回固定し直され、4 人が別々の固定で errata と台帳の行を当てた。
「誰の判定が、その後に動いた条に当たるか」は手で diff を読んで 1 人ずつ知らせた。判定は、判定した日の本文についての事実で、
条が動けばその行だけ当て直しが要る。

**使い方** (CI では回さない):
    python3 .github/scripts/moved_clauses.py BEFORE [AFTER]
        # BEFORE / AFTER は file の path か、git の版 (<rev> なら <rev> の作業中の草案・<rev>:<path> ならその path)。
        # AFTER を省くと作業中の草案。動いた条・新しい条・消えた条を出す
    python3 .github/scripts/moved_clauses.py --ledger LICENSES/ACD-1.5-UNIQUE-READING.md
        # 台帳の行（"- §x.y … ｜ 本文 <rev>" の <rev> を判定した本文とする）のうち、その条が判定の後に動いたものを出す

**条の本文**は空白を畳んで比べる（折り返しだけの差は動いたと数えない）。条の中の段 (a)〜(e) は条に含める。
**測っていないもの**: 動いた条を引く別の条の読み（`Section N.M` の参照）。--refs を付けると、動いた条を参照する条も添える。
終了コード: 動いた条（--ledger では当て直しの要る行）が 1 つ以上なら 1、無ければ 0、読めなければ 2。
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

if sys.version_info < (3, 10):
    print("ERROR: moved_clauses.py requires Python 3.10+ (got %d.%d)" % sys.version_info[:2])
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[2]
RULE = "-" * 80
REV_IN_ROW = re.compile(r"本文 `?([0-9a-f]{7,40})`?")


def working_draft() -> Path:
    d = [p for p in sorted((ROOT / "LICENSES").glob("ACD-*-DRAFT.txt"))
         if "HAS BEEN FROZEN" not in p.read_text(encoding="utf-8").split("\n", 1)[0]]
    if len(d) != 1:
        sys.exit(f"作業中の草案が 1 つに定まらない: {[p.name for p in d]}")
    return d[0]


def load(spec: str | None) -> str:
    """spec の本文。path・<rev>・<rev>:<path> のどれか。読めなければ終了コード 2 (空の本文を「全部動いた」と読まない)。"""
    if spec is None:
        return working_draft().read_text(encoding="utf-8")
    if Path(spec).exists():
        return Path(spec).read_text(encoding="utf-8")
    if ":" not in spec:
        spec = f"{spec}:{working_draft().relative_to(ROOT).as_posix()}"
    r = subprocess.run(["git", "show", spec], cwd=ROOT, text=True, capture_output=True)
    if r.returncode != 0:
        print(f"読めない: {spec} ({r.stderr.strip()[:120]})", file=sys.stderr)
        sys.exit(2)
    return r.stdout


def clauses(text: str) -> dict[str, str]:
    body = text.split("\n" + RULE + "\n", 1)[-1]
    out = {k: " ".join(v.split()) for k, v in
           re.findall(r"(?ms)^  (\d+\.\d+)\s+(.*?)(?=^  \d+\.\d+\s|^\d+\. [A-Z]|^END OF TERMS|\Z)", body)}
    if not out:
        print("条を 1 つも読めない (本文の形が変わったなら直す)", file=sys.stderr)
        sys.exit(2)
    return out


def moved(a: dict[str, str], b: dict[str, str]) -> tuple[list[str], list[str], list[str]]:
    key = lambda x: tuple(map(int, x.split(".")))
    return (sorted((k for k in a if k in b and a[k] != b[k]), key=key),
            sorted((k for k in b if k not in a), key=key), sorted((k for k in a if k not in b), key=key))


def ledger(path: Path) -> int:
    now, cache, stale, unread, rows = clauses(load(None)), {}, [], 0, 0
    for i, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        m = re.match(r"- §(\d+\.\d+)", line)
        if not m:
            continue
        rows += 1
        rev = REV_IN_ROW.search(line)
        if not rev:
            unread += 1
            continue
        if rev.group(1) not in cache:
            cache[rev.group(1)] = clauses(load(rev.group(1)))
        # 行が名指す条は先頭の 1 つとは限らない ("- §2.8・§5.3・§12.4") —— 最初の " | " までの § を全部見る
        for k in re.findall(r"§(\d+\.\d+)", line.split(" | ", 1)[0]):
            if cache[rev.group(1)].get(k) != now.get(k):
                stale.append((i, k, rev.group(1)))
    print(f"{path.name}: 行 {rows}・判定した本文を名乗らない行 {unread}・当て直しの要る (行, 条) {len(stale)}")
    for i, k, r in stale:
        print(f"  {path.name}:{i} §{k} —— 本文 {r} の後に動いた")
    return 1 if stale else 0


def main(argv: list[str]) -> int:
    if "-h" in argv or "--help" in argv or not argv:
        print(__doc__)
        return 0 if argv else 2
    if argv[0] == "--ledger":
        return ledger(Path(argv[1]))
    args = [a for a in argv if not a.startswith("--")]
    a, b = clauses(load(args[0])), clauses(load(args[1] if len(args) > 1 else None))
    ch, new, gone = moved(a, b)
    print(f"動いた条 {len(ch)}: {' '.join('§' + k for k in ch) or 'なし'}")
    print(f"新しい条 {len(new)}: {' '.join('§' + k for k in new) or 'なし'}")
    print(f"消えた条 {len(gone)}: {' '.join('§' + k for k in gone) or 'なし'}")
    if "--refs" in argv:
        refs = {k: sorted({c for c in b if c not in ch and re.search(rf"Sections? [^.;]*?\b{re.escape(k)}\b", b[c])}) for k in ch}
        for k, v in refs.items():
            if v:
                print(f"  §{k} を参照する条 (本文は動いていない): {' '.join('§' + x for x in v)}")
    return 1 if ch or new or gone else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
