#!/usr/bin/env python3
"""renumber_refs.py — 提出対象を替える日に、ドシエの条番号を CLAUSE-MAP で書き換える下書き（1 対 1 の引用だけを直し、残りを名指す）。

**なぜ在るか (2026-11-24・議題 20)**: 1.5 は番号を総替えした。提出対象を 1.4 から 1.5 へ替えると、入口・材料・想定問答の約 2,000 の
条番号が別の条を指す。手で直すと、1 対 1 の行で写し間違え、1 対 n の行で判断を落とす。

**何をするか**: 引用を 5 つに分ける。
  one       —— 対応表の行き先が 1 つ。`--apply` が書き換えるのはこれだけ
  many      —— 行き先が 2 つ以上（どの条の話かは文を読んで決める）
  gone      —— 行き先が無い（— の行）。文そのものを見直す
  versioned —— 同じ文の手前で版を名乗っている（「1.0 の §15.5」「ACD-1.4 §8.4」）。その版の番号なので動かさない
  quoted    —— *"…"* の引用・`…` の中。本文の語なので動かさない（引用そのものが新しい本文に在るかは 470b / 470c が照らす）
**判断しないもの**: 条の中身が変わった文（"§8.2 は報復条項が無いことを述べる" の言い換え）。番号だけが正しく文が偽、は人が読む。

使い方 (CI では回さない):
    python3 .github/scripts/renumber_refs.py 1.4 1.5 LICENSES/ADOPTING.md …          # 分類と下書き
    python3 .github/scripts/renumber_refs.py 1.4 1.5 --apply LICENSES/ADOPTING.md …  # one だけを書き換える
終了コード: many か gone が残れば 1、無ければ 0、対応表を読めなければ 2。
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

if sys.version_info < (3, 10):
    print("ERROR: renumber_refs.py requires Python 3.10+ (got %d.%d)" % sys.version_info[:2])
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[2]
REF = re.compile(r"(?P<head>§\s?|[Ss]ections?\s)(?P<num>\d{1,2}\.\d{1,2})(?P<sub>\([a-z]\))?(?P<more>\s*(?:,|、|・|and|to|〜|/)\s*§?\s?\d{1,2}\.\d{1,2})?")
# 版の名乗り: ACD-1.4 / 1.0 の / 1.0 §… / 1.0's / in 1.3 / ACD-1.0 to ACD-1.4。文の切れ目 (。 . ; | と改行) までしか効かない
VERSION = re.compile(r"(?:ACD-1\.\d|(?<![\d.§])1\.\d(?=\s*(?:の|は|で|から|まで|§|'s|'s|草案|draft|\)|,| §| to| and| Section)))")
BREAK = re.compile(r"[。;|]|(?<=[a-z)])\.\s")


def load_map(prev: str, cur: str) -> dict[str, list[str]]:
    p = ROOT / "LICENSES" / f"CLAUSE-MAP-{prev}-{cur}.tsv"
    if not p.exists():
        print(f"{p.name} が無い", file=sys.stderr)
        sys.exit(2)
    out: dict[str, list[str]] = {}
    for line in p.read_text(encoding="utf-8").splitlines():
        c = line.split("\t")
        m = re.match(r"(\d+\.\d+)(\([a-z]\))?", c[0])
        if not m or len(c) < 2:
            continue
        # "5.2(a)" は段の行き先、"5.2 末段" のような行は条全体の行き先にも足す
        key = m.group(0) if m.group(2) else m.group(1)
        out.setdefault(key, []).extend(x for x in re.findall(r"\d+\.\d+(?:\([a-z]\))?", c[1]))
        if m.group(2):
            out.setdefault(m.group(1), []).extend(x for x in re.findall(r"\d+\.\d+(?:\([a-z]\))?", c[1]))
    if not out:
        print(f"{p.name} から行を 1 つも読めない", file=sys.stderr)
        sys.exit(2)
    return out


def spans_to_skip(line: str) -> list[tuple[int, int]]:
    return [m.span() for m in re.finditer(r'\*"[^"]*"\*|`[^`]*`|"[^"]{20,}"|“[^”]*”', line)]


def classify(line: str, m: re.Match, cmap: dict[str, list[str]], skip: list[tuple[int, int]]) -> tuple[str, list[str]]:
    key = m.group("num") + (m.group("sub") or "")
    to = cmap.get(key) or cmap.get(m.group("num"))
    if to is None:
        return "other", []          # 対応表に無い番号 (ドシエの節 §1.206 など) は条の引用ではない
    if any(a <= m.start() < b for a, b in skip):
        return "quoted", []
    start = max([x.end() for x in BREAK.finditer(line[:m.start()])] + [0])
    if VERSION.search(line[start:m.start()]):
        return "versioned", []
    uniq = list(dict.fromkeys(to))
    if not uniq:
        return "gone", []
    if m.group("more"):
        return "many", uniq         # 列 (Sections 5.1 and 5.2) は、番号の間の語ごと組み替わりうる
    return ("one", uniq) if len(uniq) == 1 else ("many", uniq)


def run(path: Path, cmap: dict[str, list[str]], apply: bool) -> Counter:
    n, out = Counter(), []
    for i, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        skip, edits = spans_to_skip(line), []
        for m in REF.finditer(line):
            kind, to = classify(line, m, cmap, skip)
            n[kind] += 1
            if kind == "one":
                edits.append((m.start("num"), m.end("sub") if m.group("sub") else m.end("num"), to[0]))
            if kind in ("many", "gone"):
                print(f"  {path.name}:{i} [{kind}] §{m.group('num')}{m.group('sub') or ''} → {' / '.join('§' + t for t in to) or '—'}  "
                      f"…{line[max(0, m.start() - 40):m.end() + 30].strip()}…")
        for a, b, t in reversed(edits):
            line = line[:a] + t + line[b:]
        out.append(line)
    if apply and n["one"]:
        path.write_text("\n".join(out), encoding="utf-8")
    print(f"{path.name}: one {n['one']}{' (書き換えた)' if apply and n['one'] else ''}・many {n['many']}・gone {n['gone']}・"
          f"versioned {n['versioned']}・quoted {n['quoted']}")
    return n


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    if "-h" in argv or "--help" in argv or len(args) < 3:
        print(__doc__)
        return 0 if ("-h" in argv or "--help" in argv) else 2
    cmap, total = load_map(args[0], args[1]), Counter()
    for f in args[2:]:
        total += run(Path(f), cmap, "--apply" in argv)
    print(f"合計: one {total['one']}・many {total['many']}・gone {total['gone']}・versioned {total['versioned']}・quoted {total['quoted']}")
    return 1 if total["many"] or total["gone"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
