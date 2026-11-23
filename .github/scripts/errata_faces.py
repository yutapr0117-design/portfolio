#!/usr/bin/env python3
"""errata_faces.py — errata を 1 件足した (または状態を変えた) ときに、どの面に何を書けばよいかを 1 度で出す。

**なぜ在るか (2026-11-23・5e の依頼・fc)**: 5e が #3907 で errata E87 を足したとき、Check 464・468 (Still open)・
460 (v) と件数の面・469・498 (a) / (j) が、それぞれ別の面への名指しを求めた。どれも正しい要求だが、consistency の出力は
長く、どの誤りがこの E 番号のためのもので、どれが数の同期 (`sync_stated_counts.py --apply`) で消えるかを読み分けるのに
往復が要った。この道具は consistency を 1 回回し、その E 番号を名指す誤りと errata の件数の誤りだけを、面ごとに
「どこに・何を・誰が (道具か人か)」の形で並べる。何も書き換えない (--apply-counts を付けたときだけ数を同期する)。

使い方:
    python3 .github/scripts/errata_faces.py E88                 # 面の一覧を出す
    python3 .github/scripts/errata_faces.py E88 --apply-counts  # 先に件数を sync_stated_counts.py --apply で揃えてから出す

errata の行そのもの (`ACD-1.0.errata.md` の表) は先に人が書く。処置の文 (草案冒頭の Still open・errata 冒頭の英文) は
判断なので、この道具は場所と形だけを示す。
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# 誤りの文の印 → (面, 何を書くか, 誰が)。上から順に当てる
FACES = [
    (r"^ERROR: Check 464:", "作業中の版の CHANGELIST (`ACD-<版>-CHANGELIST.md`) の「## errata 由来」の表",
     "その E 番号の行を足す (| E番号 | 条 | 何が欠けているか・試作 | 状態 |)", "人"),
    (r"Still open", "作業中の草案の冒頭 (`ACD-<版>-DRAFT.txt` の「Still open in this draft:」)",
     "閉じないと決めたなら、その E 番号と処置を 1 句で足す (本文担当が書く)", "人 (本文担当)"),
    (r"\(v\) errata\.md 冒頭", "`ACD-1.0.errata.md` の冒頭の英文 (どの版で閉じたか・処置の列)",
     "閉じていない行の処置を述べる句に、その E 番号を足す", "人"),
    (r"^ERROR: Check 469:", "`ACD-1.0.errata.md` と作業中の CHANGELIST の E 番号の対応",
     "両方に同じ E 番号を置く (469 (b))", "人"),
    (r"閉鎖の印の無い .* を英文が名指していない", "確定した版の CHANGELIST の英文「What changed since 1.0」の、閉じていない errata を名指す文 (498 (j))",
     "その E 番号を、閉じていない errata の列 (E6・E10 と並ぶ所) に足す", "人"),
    (r"申告 .* / 実測|all [a-z-]+ are unrepaired|errata の数", "errata の件数を述べる文 (against・REVIEWERS・READY-TO-SUBMIT・errata 冒頭・CHANGELIST の英文)",
     "`sync_stated_counts.py --apply` が実測へ書き直す", "道具"),
]


def main(argv: list[str]) -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _lib_git_guard import require_unambiguous_origin
    require_unambiguous_origin()  # origin/main が古い作業 branch に解決されないこと (2026-11-23)
    ids = [a for a in argv if re.fullmatch(r"E\d+", a)]
    if len(ids) != 1:
        print(__doc__.split("使い方:")[1].split("errata の行そのもの")[0])
        return 2
    eid = ids[0]
    errata = (ROOT / "LICENSES" / "ACD-1.0.errata.md").read_text(encoding="utf-8")
    if not re.search(rf"^\| {eid} \|", errata, re.M):
        print(f"STOP: {eid} の行が ACD-1.0.errata.md の表に無い。先に行を足す (| {eid} | **§N.M (1.0 to 1.x) —— 見出し** | 本文 | 直す版 | 状態 |)")
        return 1
    if "--apply-counts" in argv:
        subprocess.run([sys.executable, ".github/scripts/sync_stated_counts.py", "--apply"], cwd=ROOT, check=False,
                       stdout=subprocess.DEVNULL)
    out = subprocess.run([sys.executable, ".github/scripts/check_repository_consistency.py"], cwd=ROOT,
                         capture_output=True, text=True).stdout
    errs = [ln for ln in out.splitlines() if ln.startswith(("ERROR:", "WARNING:"))]
    mine = [ln for ln in errs if re.search(rf"\b{eid}\b", ln) or (re.search(r"errata", ln, re.I) and re.search(r"\d+ / \d+|申告|unrepaired", ln))]
    if not mine:
        print(f"OK: {eid} について求められている面は無い (consistency の誤りに {eid} も errata の件数も出ない)")
        return 0
    seen = set()
    print(f"{eid} のために書く面 (consistency を 1 回回した結果):")
    for ln in mine:
        face = next((f for f in FACES if re.search(f[0], ln)), None)
        key = face[1] if face else ln[:60]
        if key in seen:
            continue
        seen.add(key)
        if face:
            print(f"  - [{face[3]}] {face[1]}: {face[2]}")
        else:
            print(f"  - [?] {ln[:200]}")
    if any(f[3] == "道具" for f in FACES if f[1] in seen) and "--apply-counts" not in argv:
        print("件数の面は --apply-counts を付けて回すと消える")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
