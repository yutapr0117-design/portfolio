#!/usr/bin/env python3
"""sync_stated_counts.py — 実測から導ける「書かれた数」を、手で直さずに書き直す。

**なぜ在るか (2026-11-15)**: 1c は草案の語数が変わるたびに 7 か所を手で直しており、同じ日に 263→281 の誤りと
597 の直し忘れが起きた。Check 460 (x) / 468 / 498 (k) は「書かれた数と実測が違う」と言えるが、直すのは人だった。
sync-sizes が §2 の行数を実測から書き直すのと同じく、この道具は場所の一覧 (`_lib_draft_counts.length_sites`) を
読んで、各場所の数を実測の値へ書き換える。照合 (Check) と書き換え (この道具) は同じ一覧を読むので食い違わない。

**場所の一覧**: 草案の語数から導出する数 —— 草案冒頭の "ACD-前版: N words, M clauses. This draft: N words, M clauses."、
CHANGELIST の「前版の N 語から +N 語」「1.0 の N 語から見ると M 語長い」「（束名、束名の N 束で +M）」と英文の
"N words from the title to *END OF TERMS* against 1.0's N, in M clauses against M"、B3 の見出しのかっこ、
SUBMISSION-MATERIALS の長さの行 (後半の「条文では N 語長いまま」を含む)。**判断の数は書き換えない**: 束の表の各行と、
草案冒頭の箇条の (+N words.) (どの変更に何語かは人が決め、Check 468n が照らす)。

使い方:
    python3 .github/scripts/sync_stated_counts.py          # 実測と違う場所を出す (書き換えない・違えば exit 1)
    python3 .github/scripts/sync_stated_counts.py --apply  # 書き換える
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib_dossier import is_against  # noqa: E402
from _lib_draft_counts import apply_sites, length_sites  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


def main(argv: list[str]) -> int:
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    sites, bad = length_sites(ROOT / "LICENSES", is_against, "all")
    if bad:
        print("\n".join(f"ERROR: {b}" for b in bad))
        return 2
    diff = [s for s in sites if s["old"] != s["new"]]
    for s in diff:
        print(f"{s['path'].relative_to(ROOT)}:{s['line']}  {s['what']}: {s['old']} -> {s['new']}")
    if "--apply" in argv and diff:
        print(f"書き換えた: {apply_sites(diff)} か所 (照らした {len(sites)} か所)")
        return 0
    print(f"照らした {len(sites)} か所のうち、実測と違う {len(diff)} か所" + ("" if not diff else " (--apply で書き換える)"))
    return 1 if diff else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
