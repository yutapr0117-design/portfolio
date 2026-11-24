#!/usr/bin/env python3
"""sync_stated_counts.py — 実測から導ける「書かれた数」を、手で直さずに書き直す。

**なぜ在るか (2026-11-15)**: 1c は草案の語数が変わるたびに 7 か所を手で直しており、同じ日に 263→281 の誤りと
597 の直し忘れが起きた。Check 460 (x) / 468 / 498 (k) は「書かれた数と実測が違う」と言えるが、直すのは人だった。
sync-sizes が §2 の行数を実測から書き直すのと同じく、この道具は場所の一覧 (`_lib_draft_counts.length_sites`) を
読んで、各場所の数を実測の値へ書き換える。照合 (Check) と書き換え (この道具) は同じ一覧を読むので食い違わない。

**場所の一覧**: 草案の語数から導出する数 —— 草案冒頭の "ACD-前版: N words, M clauses. This draft: N words, M clauses."、
CHANGELIST の「前版の N 語から +N 語」「1.0 の N 語から見ると M 語長い」「（束名、束名の N 束で +M）」と英文の
"N words from the title to *END OF TERMS* against 1.0's N, in M clauses against M"、B3 の見出しのかっこ、
SUBMISSION-MATERIALS の長さの行 (後半の「条文では N 語長いまま」を含む)。ドシエの規模の数 (2026-11-15・30 の依頼) —— 不利な事実の件数 (against の総括・REVIEWERS・READY-TO-SUBMIT・§4c)、
errata の件数 (against・REVIEWERS・READY-TO-SUBMIT・errata 冒頭の英語の数詞と閉じた番号の一覧)、worked entries の総数
(REVIEWERS・QUESTION-INDEX) (`_lib_dossier.count_sites`)。runbook §9 の追跡ファイルの数は 2026-11-23 に行から外した
(並行の衝突源だったので、Check 413 の OK 行が実測を出す)。「1.0 から何が変わったか」の英文の errata の数と § ごとの件数
(Check 498 (j)・`>` の引用で行をまたいでも照らす)。AS-OF の未読スレッドの候補・読了・残り (Check 498 (h) と同じ数え方)。REVIEWERS 冒頭のドシエ全体の語数・倍率・実測日 (Check 472m・
実測と 5% を越えて違うときだけ)。**判断の数は書き換えない**: 束の表の各行と、
草案冒頭の箇条の (+N words.) (どの変更に何語かは人が決め、Check 468n が照らす)。

使い方:
    python3 .github/scripts/sync_stated_counts.py          # 実測と違う場所を出す (書き換えない・違えば exit 1)
    python3 .github/scripts/sync_stated_counts.py --apply  # 書き換える
"""
from __future__ import annotations

import datetime
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib_dossier import count_sites, is_against  # noqa: E402
from _lib_draft_counts import apply_sites, length_sites  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


def reviewers_size_sites() -> list[dict]:
    """REVIEWERS.md 冒頭のドシエ全体の語数・倍率・実測日 (Check 472m が 10% の幅で照らし、8% で ADVISORY)。

    2026-11-15、472m の ADVISORY が鳴った (453,125 語と書き実測 492,630 語・8.0%)。数え方は文が名乗る再測の
    コマンド (rounds/ を除く LICENSES の `git ls-files` の語数)。**実測との差が 5% を越えたときだけ書き換える** (Check 472m の幅 10% (8% で ADVISORY) より狭いのは意図どおり —— 道具が先に直し、472m は回し忘れだけを止める)
    —— この 1 行は全員の増分で毎回動くので、毎回書き換えると並行 PR がこの行で衝突し続ける (8% の ADVISORY・
    10% の BLOCKING の手前で 1 回だけ動かす)。倍率は 472m と同じ割り算で、表の the licence の語数で割る。
    """
    rv = ROOT / "LICENSES" / "REVIEWERS.md"
    text = rv.read_text(encoding="utf-8")
    m = re.search(r"Measured (\d{4}-\d{2}-\d{2}), the analysis in\s+this directory[^*]*?is \*\*([\d,]+) words\*\*, "
                  r"\*\*(\d+) times the licence\*\*", text)
    lic = re.search(r"\(ACD-\d+\.\d+\.txt\) \| \*\*([\d,]+)\*\* \| the licence\b", text)
    if not m or not lic:
        return []
    ls = subprocess.run(["git", "ls-files", "-z", "LICENSES", ":!LICENSES/rounds"], cwd=ROOT, text=True,
                        capture_output=True, check=True).stdout
    real = sum(len((ROOT / f).read_text(encoding="utf-8", errors="replace").split()) for f in sorted(set(ls.split("\0"))) if f)
    said = int(m.group(2).replace(",", ""))
    line = text[:m.start()].count("\n") + 1
    if abs(said - real) <= real * 0.05:
        new_n, new_d = m.group(2), m.group(1)
    else:
        new_n, new_d = f"{real:,}", datetime.date.today().isoformat()
    # 倍率は書いた語数と表の分母から毎回導く。語数の 5% の幅に関わらない: 提出の版を切り替える日は 472h が表の分母を
    #   1.4 へ替えるので、語数が幅の内でも倍率だけがずれて 472m が RED になる (50 の問い・2026-11-15)
    lw = int(lic.group(1).replace(",", ""))
    new_x = m.group(3) if abs(int(m.group(3)) - int(new_n.replace(",", "")) / lw) <= 1 else str(round(int(new_n.replace(",", "")) / lw))
    return [{"path": rv, "line": line, "abs": True, "start": m.start(i), "end": m.end(i), "old": m.group(i), "new": v,
             "what": f"REVIEWERS のドシエ全体の{w}"}
            for i, v, w in ((1, new_d, "実測日 (語数の差が 5% を越えたときだけ)"), (2, new_n, "語数 (差が 5% を越えたときだけ)"),
                            (3, new_x, "倍率 (書いた語数 ÷ 表の the licence の語数)"))]


def asof_sites() -> list[dict]:
    """AS-OF の「候補 N 本のうち M 本を読んだ。K 本は読んでいない」(Check 498 (h) と同じ数え方・2026-11-15・50 の依頼)。

    N = THREAD-CANDIDATES の会話の数、M = READ-THREADS の行のうち候補に在る会話 (件名の key と日付の組)、K = N - M。
    safe_merge --reland が AS-OF の行の衝突で main 側を採った後、件数をここで実測へ戻す。アーカイブ無しに再現できる。
    """
    from census_decision_statements import _list_rows
    asof = ROOT / "LICENSES" / "AS-OF.md"
    text = asof.read_text(encoding="utf-8")
    m = re.search(r"候補 (\d+) 本のうち (\d+) 本を読んだ。(\d+) 本は読んでいない", text)
    if not m:
        return []
    from census_decision_statements import candidate_rows, read_rows
    cand = {(k, d) for k, d, _t in candidate_rows(ROOT / "LICENSES")}
    read = {(k, d) for k, d, _t in read_rows(ROOT / "LICENSES")} & cand
    vals = (len(cand), len(read), len(cand) - len(read))
    line = text[:m.start()].count("\n") + 1
    return [{"path": asof, "line": line, "abs": True, "start": m.start(i + 1), "end": m.end(i + 1), "old": m.group(i + 1),
             "new": str(v), "what": f"AS-OF の未読スレッドの{w}"} for i, (v, w) in enumerate(zip(vals, ("候補", "読了", "残り")))]


def defects_sites() -> list[dict]:
    """「1.0 から何が変わったか」の英文の errata の数 (Check 498 (j) が照らす・2026-11-15・30 の検証から)。

    "Of the N defects recorded against 1.0 …, N are closed: N in 1.1 to 1.3 (a, b and c) and N for the first time in 1.4."
    は `>` の引用で行をまたぐので、引用の語を 1 列につないで照らし、数の位置を元の file の位置へ戻す。値は
    prepare_version_freeze.errata_closures() (498 (j) と同じ)。§ ごとの件数の括弧も同じ関数の節の数で書き直す。
    """
    from prepare_version_freeze import errata_closures
    total, closed, _unmarked, sections = errata_closures()
    sites = []
    for p in sorted((ROOT / "LICENSES").glob("ACD-*-CHANGELIST.md")) + [ROOT / "LICENSES" / "REVIEWERS.md"]:
        text = p.read_text(encoding="utf-8")
        toks = []  # (語, file の中の始まり)
        for m in re.finditer(r"^>[ \t]?(.*)$", text, re.M):
            for t in re.finditer(r"\S+", m.group(1)):
                toks.append((t.group(0), m.start(1) + t.start()))
        joined, starts = "", []
        for w, s in toks:
            starts.append((len(joined) + (1 if joined else 0), s))
            joined += (" " if joined else "") + w

        def orig(j):  # つないだ列の位置 → file の位置
            k = max(i for i, (js, _s) in enumerate(starts) if js <= j)
            return starts[k][1] + (j - starts[k][0])

        rx = (r"Of the (\d+) defects recorded against 1\.0 .{0,80}?, (\d+) are closed: (\d+) in 1\.1 to (\d+\.\d+) "
              r"\(([\d, and]+)\) and (\d+) for the first time in (\d+\.\d+)\.(.{0,900})")
        for m in re.finditer(rx, joined):
            tgt = m.group(7)
            olds = sorted((v for v in closed if v != tgt), key=lambda x: tuple(map(int, x.split("."))))
            per = [str(len(closed[v])) for v in olds]
            per_s = ", ".join(per[:-1]) + " and " + per[-1] if len(per) > 1 else "".join(per)
            vals = {1: str(total), 2: str(sum(map(len, closed.values()))), 3: str(sum(len(closed[v]) for v in olds)),
                    5: per_s, 6: str(len(closed.get(tgt, [])))}
            for gi, v in vals.items():
                a, b = orig(m.start(gi)), orig(m.end(gi) - 1) + 1
                if text[a:b] == m.group(gi):  # 語の間で改行していない数だけ書き換える (列の括弧は行をまたぎうる)
                    sites.append({"path": p, "line": text[:a].count("\n") + 1, "abs": True, "start": a, "end": b,
                                  "old": m.group(gi), "new": v, "what": "1.0 からの変化の英文の errata の数"})
            rest_off = m.start(8)
            for sm in re.finditer(r"§(\d+) \([^()]*?, (\d+)\)", m.group(8)):
                if sm.group(1) in sections:
                    a = orig(rest_off + sm.start(2))
                    b = a + len(sm.group(2))
                    if text[a:b] == sm.group(2):
                        sites.append({"path": p, "line": text[:a].count("\n") + 1, "abs": True, "start": a, "end": b,
                                      "old": sm.group(2), "new": str(sections[sm.group(1)]),
                                      "what": f"1.0 からの変化の英文の §{sm.group(1)} の件数"})
    return sites


def main(argv: list[str]) -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _lib_git_guard import require_unambiguous_origin
    require_unambiguous_origin()  # origin/main が古い作業 branch に解決されないこと (2026-11-23)
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    sites, bad = length_sites(ROOT / "LICENSES", is_against, "all")
    sites += count_sites(ROOT / "LICENSES") + defects_sites() + reviewers_size_sites() + asof_sites()
    if bad:
        print("\n".join(f"ERROR: {b}" for b in bad))
        return 2
    diff = [s for s in sites if s["old"] != s["new"]]
    # 書き換えない判断の文の知らせ (2026-11-15・30 の検証): errata 冒頭は、閉じていない行を閉じた番号の一覧の後で
    #   名指す (Check 460 (v))。提案中か・持ち越しか・意図して残すかは人が書くので、名指されていない番号だけを出す
    from prepare_version_freeze import errata_closures
    head = next((ln for ln in (ROOT / "LICENSES" / "ACD-1.0.errata.md").read_text(encoding="utf-8").split("\n")
                 if "items are recorded" in ln), "")
    after = head.split(") are closed", 1)[-1]
    for e in [e for e in errata_closures()[2] if not re.search(rf"\b{e}\b", after)]:
        print(f"手で足す: errata 冒頭が閉じていない {e} を一覧の後で名指していない (Check 460 (v)・状態の句は人が書く)")
    for s in diff:
        print(f"{s['path'].relative_to(ROOT)}:{s['line']}  {s['what']}: {s['old']} -> {s['new']}")
    if "--apply" in argv and diff:
        print(f"書き換えた: {apply_sites(diff)} か所 (照らした {len(sites)} か所)。STATUS.md も件数を写すので "
              "`npm run status` を回し、最後に verify で Check 460 / 468 / 498 を確かめる")
        return 0
    print(f"照らした {len(sites)} か所のうち、実測と違う {len(diff)} か所" + ("" if not diff else " (--apply で書き換える)"))
    return 1 if diff else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
