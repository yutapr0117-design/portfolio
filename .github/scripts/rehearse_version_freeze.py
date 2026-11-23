#!/usr/bin/env python3
"""rehearse_version_freeze.py — 確定の道具が今の tree で確定まで届くことを、使い捨ての worktree で確かめる。

**なぜ在るか。** `prepare_version_freeze.py` は確定の日にしか走らない。本文やドシエの形が変わって道具が
壊れても、確定の日まで分からない。週次の `mutation-probe.yml` がこれを回す。

**やること**: HEAD を別の worktree に取り出し、確定の道具を走らせ、新しい file を明示パスで add して
consistency を回す。RED が「人が読んで直す」一覧 `EXPECTED` の中に収まれば成功である。一覧の外の RED、
traceback、道具の失敗は失敗で、確定の日に止まる場所が増えたことを意味する。作業ツリーは触らない。

使い方:
    python3 .github/scripts/rehearse_version_freeze.py
"""
from __future__ import annotations

import datetime
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# 確定の直後に残って正しい RED。直し方は docs/files/.github/scripts/prepare_version_freeze.py.md の表にある。
# 2026-11-20: 予行が提出の前提の止め (段 6b) で毎週止まっていた間に、確定の道具が「人が直す」と出す 460 (x) (B3 の見出しの
#   「N.M 草案は」) と、版に固有の anchor を持つ 444・468x・498 の mutation が加わっていた (main でも同じ RED を確かめた)
EXPECTED = {"362", "444m", "460"}
# 362 は番号が同じまま別の mutation の anchor でも RED になるので、orphan の数が確定の道具の一覧の数と同じかを見る。
#   2026-11-08 の予行で、Check 496 の mutation が空の次版 CHANGELIST を指して 362 に加わっていたが、番号では見えなかった。


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, text=True, capture_output=True).stdout


def rehearse(tree: Path) -> list[str]:
    # 予行は確定の仕組みが届くかを見るので、提出の前提 (段 6b の 30 日・ゲート 6c) は外す (2026-11-20: 前提の止めが入った後、
    #   予行は毎週ここで止まり、仕組みの壊れを見ていなかった)。前提の止めそのものは prepare_version_freeze の gate が持つ
    tool = subprocess.run([sys.executable, ".github/scripts/prepare_version_freeze.py", "--date", datetime.date.today().isoformat(),
                           "--not-for-submission"],
                          cwd=tree, text=True, capture_output=True)
    if tool.returncode != 0:
        return [f"確定の道具が止まった: {(tool.stderr or tool.stdout)[-300:]}"]
    # 付録に変更の一覧の箇条が逐語で入ったか (2026-11-20・30: 一覧を草案の外 CHANGES-ACD-N.M.txt へ出した後、道具が草案の
    #   ファイルだけを読むと付録から一覧が落ちる)。確定した版は作業中の草案の版 (予行の木の前の状態) から読む
    ver = re.match(r"ACD-(\d+\.\d+)-DRAFT", next(p for p in sorted((ROOT / "LICENSES").glob("ACD-*-DRAFT.txt"))
                                                if "HAS BEEN FROZEN" not in p.read_text(encoding="utf-8").split("\n", 1)[0]).name).group(1)
    cl = (tree / "LICENSES" / f"ACD-{ver}-CHANGELIST.md").read_text(encoding="utf-8")
    app = cl.split("## 付録: 確定時点の草案ヘッダ（逐語）", 1)[-1] if "## 付録: 確定時点の草案ヘッダ（逐語）" in cl else ""
    # 状態の箇条 ("    * It has had no legal review") も同じ形なので、「Changes in this draft」より後の箇条だけを数える
    lst = app.split("Changes in this draft", 1)[1] if "Changes in this draft" in app else ""
    if len(re.findall(r"^    \* (?!ACD-\d+\.\d+: )", lst, re.M)) == 0:
        return [f"確定した ACD-{ver} の CHANGELIST の付録に、変更の一覧の箇条が無い (草案の外の一覧を写していない)"]
    major, minor = ver.split(".")
    if not (tree / "LICENSES" / f"CHANGES-ACD-{major}.{int(minor) + 1}.txt").exists():
        return [f"次版の変更の一覧 CHANGES-ACD-{major}.{int(minor) + 1}.txt が作られていない"]
    applied = re.search(r"^SPDX-License-Identifier: (\S+)$", (ROOT / "LICENSE").read_text(encoding="utf-8"), re.M).group(1)
    for name in ("LICENSE", "llms-full.txt"):
        if not re.search(rf"this\s+repository\s+applied\s+{re.escape(applied)}\b", (tree / name).read_text(encoding="utf-8")):
            return [f"{name} の適用の履歴が前の版 {applied} を述べていない"]
    # 日付つきの追記・訂正の中の歴史を書き換えていないか (2026-11-23・cd が見つけた: 道具が「**2026-10-29 追記**: … いまの作業場は
    #   `ACD-1.4-DRAFT.txt`」を 1.5 へ置換していた)。次版の草案は確定の日に生まれるので、それより前の日付の印に続く同じ行の中で
    #   次版の草案を名指すのは書き換えられた歴史である。468k は行の最後の名前しか見ないので、consistency では見えない
    today = datetime.date.today().isoformat()
    nxt_draft = f"ACD-{major}.{int(minor) + 1}-DRAFT.txt"
    rewritten = []
    for path in git("diff", "--name-only", "HEAD", cwd=tree).split():
        if not path.endswith(".md") or not (tree / path).exists():
            continue
        for n, line in enumerate((tree / path).read_text(encoding="utf-8").split("\n"), 1):
            for hit in re.finditer(re.escape(nxt_draft), line):
                marks = re.findall(r"(\d{4}-\d{2}-\d{2})[^|]{0,12}?(?:追記|訂正)", line[:hit.start()])
                if marks and marks[-1] < today:
                    rewritten.append(f"{path}:{n} ({marks[-1]})")
    if rewritten:
        return [f"確定の道具が日付つきの追記の中の作業場の名前を {nxt_draft} へ書き換えた: {rewritten[:5]}"]
    git("add", "--", *git("ls-files", "--others", "--exclude-standard", cwd=tree).split(), cwd=tree)
    check = subprocess.run([sys.executable, ".github/scripts/check_repository_consistency.py"], cwd=tree, text=True, capture_output=True)
    out = check.stdout + check.stderr
    if "Traceback" in out:
        return [f"consistency が traceback で止まった: {out[-300:]}"]
    red = {m.group(1) for m in re.finditer(r"^ERROR: Check (\S+?):", out, re.M)}
    print(f"確定の直後の RED: {sorted(red)}")
    problems = [f"一覧の外の RED: Check {n}" for n in sorted(red - EXPECTED)]
    m362 = re.search(r"^ERROR: Check 362: orphaned mutation find-anchor\(s\) \((\d+) 件\): (.*)$", out, re.M)
    if "362" in red and not m362:
        problems.append("Check 362 の RED の形が読めない (名指された mutation を照合できない)")
    elif m362:
        # 362 の文は先頭の 5 件しか名指さないので、全件は確定の道具が出す一覧 (orphan_mutations の "  - <名>") から読む (2026-11-20)
        names = [ln[4:] for ln in tool.stdout.splitlines() if ln.startswith("  - Check ")]
        # 作業中の版のファイル (CHANGELIST・CHANGES・逐条の下書き・記述子の下書き) を打つ mutation は、確定で次版の空のファイルに
        #   替わるので的を外す (道具が退役の候補として名を出す)。予行が見るのは、362 の orphan がすべて道具の一覧に在ること
        #   (一覧の外の orphan = 道具が知らずに壊した anchor)。2026-11-20 に 18 件 (468n・468y・468z・471 (d)・460 (x)・444・498 …)
        if len(names) != int(m362.group(1)):
            problems.append(f"Check 362 の orphan {m362.group(1)} 件と、確定の道具が退役の候補に出した一覧 {len(names)} 件が合わない "
                            "(道具の一覧の外で anchor が壊れた)")
    return problems


def main() -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _lib_git_guard import require_unambiguous_origin
    require_unambiguous_origin()  # origin/main が古い作業 branch に解決されないこと (2026-11-23)
    with tempfile.TemporaryDirectory() as parent:
        tree = Path(parent) / "rehearsal"
        git("worktree", "add", "--detach", "--quiet", str(tree), "HEAD")
        try:
            problems = rehearse(tree)
        finally:
            git("worktree", "remove", "--force", str(tree))
    for problem in problems:
        print(f"ERROR: {problem}")
    if not problems:
        print("OK: 確定の道具は確定まで届き、残る RED は人が読む一覧の中に収まった")
    return 1 if problems else 0


if __name__ == "__main__":
    if sys.version_info < (3, 10):
        sys.exit("Python 3.10 or later is required")
    sys.exit(main())
