#!/usr/bin/env python3
"""clause_ref_lint.py — 新しく書いた行の「版を名乗らない曖昧な条番号」を出す (ADVISORY・手で回す)。

**なぜ在るか (2026-11-15・30 の依頼)**: 1.0 と 1.1 以降は §1 と §15 / §16 の条番号の中身が違う (1.0 の §15.7 は準拠法なし、
1.4 の §15.7 は無い / 1.0 の §15.3 と 1.4 の §15.3 は別の条)。2f の §1.210 は §15.7 と §15.3 を取り違えかけた
(against #221 の型)。ドシエ全体を照らすと 856 か所が出て、大半は文書全体が 1 つの版を前提にしているので Check に
できない (30 と合意して見送った)。そこで、その PR で足した行だけを見る。

**曖昧な番号**: `ACD-1.1-CHANGELIST.md` §0.5 の対応表 (make_redline.py と同じ読み方) で、1.0 の番号が別の番号へ動いたか
消えたもの、と、後の版でその番号に別の条が入ったもの。**版の名乗り**: 同じ段落か同じ表の行に「1.0」「ACD-1.4」
「1.4 草案」「1.4 draft」などの版の語があれば名乗ったとみなす (register の行は 1 行が長く、名乗りが前の方にある)。

出すもの: file:行・番号・その番号の 1.0 の条の頭と、いまの草案の条の頭 (取り違えかを、その場で決められるように)。
exit は常に 0 (ADVISORY)。版を名に持つ文書 (`ACD-1.4-CHANGELIST.md`・`ACD-1.4-…-TRIAL.md` など、`ACD-N.M-` で始まる file) は
文書全体がその版の番号なので読まない。冒頭 40 行で "Clause numbers are those of …" / 「条番号は ACD-N.M」と文書全体の版を
宣言している文書 (QUESTIONS-FOR-COUNSEL・objection-map など) も読まない。読むのは 1.0 のドシエ (`ACD-1.0.*.md`) と入口の文書 (REVIEWERS など)。

使い方:
    python3 .github/scripts/clause_ref_lint.py                     # origin/main からの差分で足した行
    python3 .github/scripts/clause_ref_lint.py --since HEAD~3      # 比べる元を変える
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_redline import map_from_10, parts  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
VER = re.compile(r"(?:ACD-)?1\.\d+(?:\s*(?:草案|draft))?(?=\s|§|の|$|[）),、。])|version 1\.\d", re.I)


def ambiguous() -> set[str]:
    m = map_from_10()
    amb = {k for k, v in m.items() if v != k}
    amb |= {v for k, v in m.items() if v and v != k}
    return amb


def heads(ver_text: str) -> dict[str, str]:
    return {k: " ".join(v.split()[:12]) for k, v in parts(ver_text).items() if re.fullmatch(r"\d+\.\d+", k)}


def added_lines(since: str) -> list[tuple[str, int]]:
    out = subprocess.run(["git", "-c", "core.quotepath=off", "diff", "-U0", "--no-color", since, "--", "LICENSES/*.md"],
                         cwd=ROOT, text=True, capture_output=True, check=True).stdout
    res, f, ln = [], None, 0
    for line in out.split("\n"):
        if line.startswith("+++ "):
            f = line[6:] if line.startswith("+++ b/") else None
        elif line.startswith("@@"):
            ln = int(re.search(r"\+(\d+)", line).group(1))
        elif line.startswith("+") and f and "/rounds/" not in f and not re.search(r"/ACD-\d+\.\d+-", f):
            res.append((f, ln))
            ln += 1
        elif not line.startswith("-"):
            ln += 1
    return res


def block(lines: list[str], i: int) -> str:
    """表の行ならその行、そうでなければ空行で区切った段落。"""
    if lines[i].startswith("|"):
        return lines[i]
    a = i
    while a > 0 and lines[a - 1].strip():
        a -= 1
    b = i
    while b + 1 < len(lines) and lines[b + 1].strip():
        b += 1
    return "\n".join(lines[a:b + 1])


def main(argv: list[str]) -> int:
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    since = argv[argv.index("--since") + 1] if "--since" in argv else "origin/main"
    amb = ambiguous()
    h10 = heads((ROOT / "LICENSES" / "ACD-1.0.txt").read_text(encoding="utf-8"))
    drafts = [p for p in sorted((ROOT / "LICENSES").glob("ACD-*-DRAFT.txt"))
              if "HAS BEEN FROZEN" not in p.read_text(encoding="utf-8").split("\n", 1)[0]]
    hd = heads(drafts[0].read_text(encoding="utf-8")) if drafts else {}
    dv = drafts[0].name.split("-")[1] if drafts else "?"
    rx = re.compile(r"§(%s)(?![\d.])" % "|".join(re.escape(a) for a in sorted(amb, key=len, reverse=True)))
    hits = 0
    cache: dict[str, list[str]] = {}
    declared = re.compile(r"Clause numbers are those of|条番号は\s*(?:ACD-)?\d")
    for f, ln in added_lines(since):
        lines = cache.setdefault(f, (ROOT / f).read_text(encoding="utf-8").split("\n"))
        # 冒頭で文書全体の版を宣言している文書は、その版の番号で書かれている (QUESTIONS-FOR-COUNSEL は ACD-1.3、
        #   objection-map は ACD-1.0・30 の提案 2026-11-15)。版を名に持つ文書と同じく読まない
        if any(declared.search(x) for x in lines[:40]):
            continue
        line = lines[ln - 1]
        if not rx.search(line) or VER.search(block(lines, ln - 1)):
            continue
        for m in rx.finditer(line):
            hits += 1
            k = m.group(1)
            print(f"{f}:{ln}  §{k} (同じ段落・表の行に版の名乗りが無い)")
            print(f"    1.0 §{k}: {h10.get(k, '(1.0 に無い)')}")
            print(f"    {dv} §{k}: {hd.get(k, f'({dv} に無い)')}")
    print(f"ADVISORY: {since} から足した行で、版を名乗らない曖昧な条番号 {hits} 件 (曖昧な番号 {len(amb)} 個: "
          f"{', '.join(sorted(amb, key=lambda x: tuple(map(int, x.split('.')))))})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
