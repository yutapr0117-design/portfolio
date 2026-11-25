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

    python3 .github/scripts/moved_clauses.py --effect-diff
        # 凍結の門「効果の差の読み」の記録 (ACD-N.M-EFFECT-DIFF.md の印) が、いまの候補についてのものかを見る。印に書く sha256 も出す

    python3 .github/scripts/moved_clauses.py --pin
        # 出す版を替える前の門 (ACD-N.M-GATE.md・議題 31) の印を、いまの草案・一覧・文で書き直す (動いたら since は今日 = 数え直し)

**条の本文**は空白を畳んで比べる（折り返しだけの差は動いたと数えない）。条の中の段 (a)〜(e) は条に含める。
**測っていないもの**: 動いた条を引く別の条の読み（`Section N.M` の参照）。--refs を付けると、動いた条を参照する条も添える。
終了コード: 動いた条（--ledger では当て直しの要る行）が 1 つ以上なら 1、無ければ 0、読めなければ 2。
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

if sys.version_info < (3, 10):
    print("ERROR: moved_clauses.py requires Python 3.10+ (got %d.%d)" % sys.version_info[:2])
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[2]
RULE = "-" * 80
STAMP = re.compile(r"<!-- EFFECT-DIFF: base=ACD-(?P<base>\d+\.\d+) commit=(?P<commit>[0-9a-f]{7,40}) body-sha256=(?P<body>[0-9a-f]{64}) "
                   r"readers=(?P<readers>\d+) read-sha256=(?P<read>[0-9a-f]{64}) reapplied=(?P<re>none|[\d.,]+) high=(?P<high>\d+) "
                   r"unsorted=(?P<unsorted>\d+) -->")
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


def body_sha(text: str) -> str:
    """区切り線の後の本文の sha256 (空白を畳む —— 折り返しの直しは候補を替えない)。"""
    return hashlib.sha256(" ".join(text.split("\n" + RULE + "\n", 1)[-1].split()).encode()).hexdigest()


def effect_diff_gate(v: str, prev: str, draft: str) -> list[str]:
    """凍結の門「効果の差の読み」(2026-11-24・6c と 3f の提案): ACD-<v>-EFFECT-DIFF.md の印が、いまの候補についてのものか。

    errata と UNIQUE-READING の回帰は「過去に問題になった語」しか見ない。書き直した 1.5 では、4 人の回帰で「開いた 0」の後に、
    ドシエを持たない読み手が 2 本の本文だけを読んで記録の無い落ちを 11 件出した。差の数は数えない (1 回の読みの量に依る)。
    見るのは「記録が在り、いまの候補の本文についてのもので、仕分けの無い差が 0」まで。仕分けの正しさは人が読む。
    high は読みが残した HIGH の実数。GATE.md (出す版を替える前の門・議題 31) に合格の結果が在る版では、結果の listed-high と同じ数で
    通り、無い版では 0 だけが通る (_lib_gate_pin.high_problem)。0 と書く誘因を作らないため、残すと決めた HIGH も数に入れる。
    """
    p = ROOT / "LICENSES" / f"ACD-{v}-EFFECT-DIFF.md"
    if not p.exists():
        return [f"{p.name} が無い (候補と ACD-{prev} の 2 本だけを、ドシエを持たない読み手に読ませ、差を 1 件ずつ仕分けた記録)"]
    m = STAMP.search(p.read_text(encoding="utf-8"))
    if not m:
        return [f"{p.name} に印 (<!-- EFFECT-DIFF: base=ACD-x.y commit=… body-sha256=… readers=N read-sha256=… reapplied=none|2.3,… "
                "high=N unsorted=N -->) が無い"]
    out = []
    if m["base"] != prev:
        out.append(f"{p.name} の基準が ACD-{m['base']} (直前の凍結版は ACD-{prev})")
    if int(m["readers"]) < 2:
        out.append(f"{p.name} の読み手が {m['readers']} 体 (独立の 2 体が要る・議題 24)")
    from _lib_gate_pin import gate_result, high_problem
    if hp := high_problem(int(m["high"]), gate_result(v)):
        out.append(f"{p.name}: {hp}")
    if int(m["unsorted"]):
        out.append(f"{p.name} に仕分けの無い差が {m['unsorted']} 件ある")
    # 読み手が読んだ固定と候補が違うなら、動いた条を当て直した印が要る。読んだ固定は repo に無いことがあるので、条の列が正しいかは見えない
    redo = [] if m["re"] == "none" else [x for x in m["re"].split(",") if x]
    if m["read"] != m["body"] and not redo:
        out.append(f"{p.name}: 読んだ固定と候補の本文が違うのに、当て直した条 (reapplied) が無い")
    if len(redo) > 10:
        out.append(f"{p.name}: 読んだ後に {len(redo)} 条が動いた。10 条を超えるので、読み手に読み直させる")
    bad_re = [x for x in redo if x not in clauses(draft)]
    if bad_re:
        out.append(f"{p.name}: reapplied の条 {bad_re} が候補に無い")
    if m["body"] != body_sha(draft):
        a, b = clauses(load(m["commit"])), clauses(draft)
        ch, new, gone = moved(a, b)
        n = len(ch) + len(new) + len(gone)
        out.append(f"{p.name} の後に候補が動いた: 条 {n} 個 ({' '.join('§' + k for k in ch + new + gone) or '条の外 (見出し・題名)'})。"
                   + ("10 条を超えるので、読み手に読み直させる" if n > 10 else "動いた条だけを当て直し、印を書き直す"))
    return out


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
    if argv[0] == "--pin":
        from _lib_gate_pin import repin
        print(repin())
        return 0
    if argv[0] == "--effect-diff":
        d = working_draft()
        v = re.match(r"ACD-(\d+\.\d+)-DRAFT", d.name).group(1)
        prev = max((re.match(r"ACD-(\d+\.\d+)\.txt$", p.name).group(1) for p in (ROOT / "LICENSES").glob("ACD-*.txt")
                    if re.match(r"ACD-\d+\.\d+\.txt$", p.name)), key=lambda x: tuple(map(int, x.split("."))))
        bad = effect_diff_gate(v, prev, d.read_text(encoding="utf-8"))
        print(f"候補 {d.name} の body-sha256 {body_sha(d.read_text(encoding='utf-8'))}")
        print("\n".join(f"  - {x}" for x in bad) if bad else "OK: 効果の差の読みは、いまの候補についてのもので、仕分けの無い差は 0")
        return 1 if bad else 0
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
