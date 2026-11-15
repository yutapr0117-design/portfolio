#!/usr/bin/env python3
"""safe_merge.py — PR を「いまの main に重ねた形」で consistency check に通してから rebase merge する。

**なぜ在るか (2026-11-15)**: 5 人が並行して PR を merge すると、それぞれの PR の CI は緑でも、2 本がほぼ同時に
merge された main は赤になりうる。同じ日に実際に起きた: rounds/ に受領文を足す 2 本がどちらも README の在庫見出しを
「444」にして緑で merge され、main の Check 465 が 444 / 445 で赤になり、その後に出た無関係な PR (#3060) の CI まで
落ちた。PR の CI は PR を出した時点の main と重ねて回るので、merge の直前の main とは重ねていない。

**何をするか**: (1) origin/main と PR の head を取得する。(2) 一時的な worktree (detached) を origin/main に作り、PR の head
を merge する (衝突したら止まる)。(3) その worktree で `check_repository_consistency.py` を回す (verify の全段ではなく、
並行の merge で壊れるのは数と参照の照合なので consistency に絞る)。(4) 緑で、PR の CI も緑で、取得してから main が
動いていなければ `gh pr merge --rebase` する (動いていたら新しい main に重ね直して最大 3 回まで回し直す)。どこかで止まったら理由を出して非 0 で終わる。worktree は必ず消す。

**しないこと**: force-push・rebase した branch の push・auto merge。main が 3 回続けて動いたら止まる。

使い方:
    python3 .github/scripts/safe_merge.py 3060            # 確かめて merge する
    python3 .github/scripts/safe_merge.py 3060 --dry-run  # 確かめるだけ
    python3 .github/scripts/safe_merge.py 3060 --reland   # 衝突したら、数の行だけなら新しい branch へ載せ直して新しい PR を出す

**--reland (2026-11-15・50 の依頼)**: 同じ日に 5 本が「main 側も動かした数の行」(rounds/README の在庫・長さの行・AS-OF の
件数) だけで衝突し、そのたびに手で載せ直した。--reland は、いまの main から `<branch>-reland` を作って PR の commit を
cherry-pick し、衝突の塊を次の 2 つに限って解く: 数だけが違う塊 (main 側を採り、後で sync_stated_counts.py --apply が
実測から書き直す) と、両側が行を足しただけの塊 (表の行・READ-THREADS の行。両方を残す)。それ以外の塊があれば何も
しないで止まる。載せ直した形で consistency を回し、緑なら push して新しい PR を出し、元の PR を閉じる。merge はしない
(新しい PR の CI を待ってから safe_merge.py で入れる)。push 済みの branch は rebase しない規則を守るための形である。
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(cmd: list[str], cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess:
    # git fetch は一時的に落ちる (2026-11-15・#3198 で CI 緑の後の fetch が exit 1 → traceback で merge されなかった。
    #   手で回し直すと通った)。fetch だけ 3 回まで間隔を空けて試す。他のコマンドは 1 回 (merge を 2 度打たない)
    tries = 3 if cmd[:2] == ["git", "fetch"] else 1
    for i in range(tries):
        r = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
        if r.returncode == 0 or i == tries - 1:
            break
        time.sleep(10 * (i + 1))
    if check and r.returncode:
        raise subprocess.CalledProcessError(r.returncode, cmd, r.stdout, r.stderr)
    return r


def overlay_check(pr: str, head: str, base: str) -> tuple[bool, str]:
    """一時的な worktree を base に作り head を merge して consistency を回す。worktree は必ず消す。"""
    tmp = Path(tempfile.mkdtemp(prefix=f"safe-merge-{pr}-"))
    wt = tmp / "wt"
    try:
        run(["git", "worktree", "add", "-q", "--detach", str(wt), base])
        m = run(["git", "-c", "user.name=safe-merge", "-c", "user.email=safe-merge@localhost",
                 "merge", "-q", "--no-edit", head], cwd=wt, check=False)
        if m.returncode:
            return False, (f"STOP: #{pr} はいまの main ({base[:8]}) と衝突する。新しい branch へ cherry-pick して出し直す\n"
                           f"{m.stdout}{m.stderr}")
        c = run([sys.executable, ".github/scripts/check_repository_consistency.py"], cwd=wt, check=False)
        errors = [ln[:300] for ln in c.stdout.splitlines() if ln.startswith("ERROR:")]
        if c.returncode or errors:
            return False, (f"STOP: #{pr} をいまの main ({base[:8]}) に重ねると consistency が赤 ({len(errors)} 件):\n"
                           + "\n".join(errors))
        return True, f"OK: #{pr} ({head[:8]}) をいまの main ({base[:8]}) に重ねて consistency は緑"
    finally:
        run(["git", "worktree", "remove", "--force", str(wt)], check=False)
        shutil.rmtree(tmp, ignore_errors=True)


_HUNK = re.compile(r"^<<<<<<< [^\n]*\n(.*?)^=======\n(.*?)^>>>>>>> [^\n]*\n", re.M | re.S)


_ASOF_ROW = "| **未読スレッドの残り** |"
_RECENT = re.compile(r"（直近の 1 件: (.*?)）。 \*\*それより前の")
MOVED_RECENT: list[str] = []  # AS-OF の行の衝突で main 側を採ったとき、PR 側の「直近の 1 件」(LOG へ移す)


def resolve_numbers_only(text: str) -> tuple[str | None, list[str]]:
    """衝突の塊を、数だけが違う塊 (main 側を採る) と、両側が行を足しただけの塊 (両方を残す) に限って解く。

    返り値: (解いた本文 か 解けなければ None, 解けなかった塊の頭)。数は後で sync_stated_counts.py --apply が実測から
    書き直すので、main 側の数を採ってよい。行を足しただけの塊は在庫表の行・READ-THREADS の行の形で、順は main → PR。
    """
    bad = []

    def fix(m):
        ours, theirs = m.group(1), m.group(2)  # cherry-pick では ours = main 側 (HEAD)、theirs = PR の commit
        if re.sub(r"\d", "0", ours) == re.sub(r"\d", "0", theirs):
            return ours
        if not ours.strip() or not theirs.strip():
            return ours + theirs
        o, t = ours.splitlines(keepends=True), theirs.splitlines(keepends=True)
        # AS-OF の「未読スレッドの残り」の行 (2026-11-15・50 の依頼): 5 人の record_read が毎回この 1 行を書き換える。
        #   main 側を採り、PR 側の「直近の 1 件」は LOG の先頭へ移す (reland が書く)。件数は sync_stated_counts が
        #   READ-THREADS と THREAD-CANDIDATES から導き直す (498 (h) と同じ数え方)
        if len(o) == len(t) == 1 and o[0].startswith(_ASOF_ROW) and t[0].startswith(_ASOF_ROW):
            mo, mt = _RECENT.search(o[0]), _RECENT.search(t[0])
            if mt and (not mo or mo.group(1) != mt.group(1)):
                MOVED_RECENT.append(mt.group(1))
            return ours
        if all(ln.startswith("|") for ln in o + t) or all(re.match(r"\d{4}-\d{2}-\d{2}\t", ln) for ln in o + t):
            return ours + "".join(ln for ln in t if ln not in o)
        # READ-THREADS-LOG の先頭の項目 (`- …` と空行): 5 人が同じ位置に 1 項目ずつ挿す。両方を残す (main → PR の順)
        if all(ln.startswith("- ") or not ln.strip() for ln in o + t):
            new = [ln for ln in t if ln.strip() and ln not in o and text.count(ln) < 2]  # main が既に持つ項目は足さない
            return ours + "".join(ln + ("" if ln.endswith("\n\n") else "\n") for ln in new)
        bad.append(ours.splitlines()[0][:80] if ours.strip() else theirs.splitlines()[0][:80])
        return m.group(0)

    out = _HUNK.sub(fix, text)
    return (None if bad else out), bad


def reland(pr: str, info: dict) -> int:
    """衝突した PR を、いまの main から新しい branch へ cherry-pick し、数の行だけの衝突を解いて新しい PR を出す。

    50 の依頼 (2026-11-15): 同じ日に 5 本が「main 側も動かした数の行」(rounds/README の在庫・長さの行・AS-OF の件数) だけで
    衝突し、そのたびに作者か 50 が手で載せ直した。push 済みの branch は rebase しない規則なので、新しい branch と新しい PR を
    作り、元の PR は閉じる (merge はしない —— 新しい PR の CI を待って safe_merge で入れる)。数以外の衝突があれば何もしないで止まる。
    """
    run(["git", "fetch", "-q", "origin", "main", info["headRefName"]])
    commits = run(["git", "rev-list", "--reverse", f"origin/main..{info['headRefOid']}"]).stdout.split()
    new = f"{info['headRefName']}-reland"
    # 統合役 (50) と作者が同時に回すと、2 人目は既在の branch で `worktree add -b` が落ちて traceback になった
    #   (2026-11-15・#3138)。先に local / remote の branch と、それを head にする open PR を見て、在れば止まる
    open_pr = json.loads(run(["gh", "pr", "list", "--head", new, "--state", "open", "--json", "number"]).stdout or "[]")
    local = run(["git", "rev-parse", "--verify", "--quiet", f"refs/heads/{new}"], check=False).returncode == 0
    remote = bool(run(["git", "ls-remote", "--heads", "origin", new], check=False).stdout.strip())
    if open_pr or local or remote:
        where = f"#{open_pr[0]['number']}" if open_pr else ("remote の branch" if remote else "local の branch")
        print(f"STOP: 既に載せ直し中: {new} ({where})。そちらの CI を待って safe_merge する")
        return 0
    tmp = Path(tempfile.mkdtemp(prefix=f"reland-{pr}-"))
    wt = tmp / "wt"
    ok = False
    try:
        run(["git", "worktree", "add", "-q", "-b", new, str(wt), "origin/main"])
        for c in commits:
            r = run(["git", "cherry-pick", c], cwd=wt, check=False)
            if r.returncode == 0:
                continue
            files = [f for f in run(["git", "diff", "-z", "--name-only", "--diff-filter=U"], cwd=wt).stdout.split("\0") if f]
            for f in files:
                solved, bad = resolve_numbers_only((wt / f).read_text(encoding="utf-8"))
                if solved is None:
                    print(f"STOP: {f} に数以外の衝突がある ({bad})。手で載せ直す")
                    run(["git", "cherry-pick", "--abort"], cwd=wt, check=False)
                    return 1
                (wt / f).write_text(solved, encoding="utf-8")
                run(["git", "add", f], cwd=wt)
            while MOVED_RECENT:  # AS-OF の行で main 側を採ったので、PR 側の直近の 1 件を LOG の先頭の項目にする
                log = wt / "LICENSES" / "READ-THREADS-LOG.md"
                lt = log.read_text(encoding="utf-8")
                h = re.search(r"^## \d{4}-\d{2}-\d{2} の読了[^\n]*\n\n", lt, re.M)
                item = f"- {MOVED_RECENT.pop(0)}\n\n"
                if h and item not in lt:
                    log.write_text(lt[:h.end()] + item + lt[h.end():], encoding="utf-8")
                    run(["git", "add", str(log)], cwd=wt)
            run([sys.executable, ".github/scripts/sync_stated_counts.py", "--apply"], cwd=wt, check=False)
            run(["git", "add", "-u"], cwd=wt)
            if run(["git", "diff", "--cached", "--quiet"], cwd=wt, check=False).returncode == 0:
                # 件数だけの commit は、main 側を採って sync で導き直すと変更が残らない。--continue は "nothing to commit" で
                #   落ちる (2026-11-15・50 が #3244 で再現)。sync が同じ数を導くので、その commit は落としてよい
                run(["git", "cherry-pick", "--skip"], cwd=wt)
                continue
            run(["git", "-c", "core.editor=true", "cherry-pick", "--continue"], cwd=wt)
        sync = run([sys.executable, ".github/scripts/sync_stated_counts.py", "--apply"], cwd=wt, check=False)
        if "書き換えた" in sync.stdout:
            run(["git", "add", "-u"], cwd=wt)
            run(["git", "commit", "-q", "-m", "chore: 載せ直しの後に、実測から導ける数を sync_stated_counts.py --apply で書き直す"],
                cwd=wt)
        c = run([sys.executable, ".github/scripts/check_repository_consistency.py"], cwd=wt, check=False)
        errors = [ln[:200] for ln in c.stdout.splitlines() if ln.startswith("ERROR:")]
        if errors:
            print("STOP: 載せ直した形で consistency が赤。手で直す:\n" + "\n".join(errors))
            return 1
        run(["git", "push", "-q", "-u", "origin", new], cwd=wt)
        title = json.loads(run(["gh", "pr", "view", pr, "--json", "title"]).stdout)["title"]
        url = run(["gh", "pr", "create", "-B", "main", "-H", new, "-t", title, "-b",
                   f"#{pr} をいまの main へ載せ直したもの (safe_merge.py --reland)。数の行だけの衝突は main 側を採り、"
                   "sync_stated_counts.py --apply で実測から書き直した。行を足しただけの衝突は両方を残した。"]).stdout.strip()
        run(["gh", "pr", "close", pr, "-c", f"いまの main と数の行で衝突したので {url} に載せ直しました (safe_merge.py --reland)。"])
        print(f"RELANDED: #{pr} → {url} (CI を待ってから safe_merge.py で merge する)")
        ok = True
        return 0
    finally:
        run(["git", "worktree", "remove", "--force", str(wt)], check=False)
        shutil.rmtree(tmp, ignore_errors=True)
        if not ok:  # 途中で止まったら作りかけの branch を消す (worktree を外してからでないと消せない)
            run(["git", "branch", "-D", new], check=False)


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1 or not args[0].isdigit() or "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0 if ("-h" in argv or "--help" in argv) else 2
    pr, dry = args[0], "--dry-run" in argv
    info = json.loads(run(["gh", "pr", "view", pr, "--json", "state,headRefName,headRefOid,statusCheckRollup"]).stdout)
    if info["state"] != "OPEN":
        print(f"STOP: #{pr} は {info['state']}")
        return 1
    bad_ci = [f'{c.get("name")}={c.get("conclusion") or c.get("status") or c.get("state")}' for c in info["statusCheckRollup"]
              if (c.get("conclusion") or c.get("state")) not in ("SUCCESS", "SKIPPED", "NEUTRAL")]
    # Architecture のパイプライン (validate-level-constraints) が起動しないことがある (trigger の取りこぼし・2026-11-15 に
    #   4 回)。CodeQL 系だけが緑だと「CI 緑」に見えるので、検査の本体が checks に無ければ止まる (50 の提案)
    if not any(c.get("name") == "validate-level-constraints" for c in info["statusCheckRollup"]):
        # 起動しない理由の多くは衝突 (2026-11-15・50 の診断): base と衝突する PR には GitHub が merge の参照を作れず、
        #   pull_request の workflow を起動しない。push の時点で main が先に動き、数の行で衝突していた (#3230・#3231 ほか・
        #   空の commit が効かなかったのもこれ)。merge-tree で衝突を見て、衝突なら --reland へ回す
        run(["git", "fetch", "-q", "origin", "main", info["headRefName"]])
        mt = run(["git", "merge-tree", "--write-tree", "--name-only", "origin/main", info["headRefOid"]], check=False)
        if mt.returncode == 1:
            files = [ln for ln in mt.stdout.splitlines()[1:] if ln and not ln.startswith(("Auto-merging", "CONFLICT"))]
            print(f"#{pr} は Architecture pipeline が起動していない —— いまの main と衝突している ({', '.join(files[:4])})。"
                  "GitHub は衝突する PR の workflow を起動しない")
            if "--reland" in argv:
                return reland(pr, info)
            print("STOP: --reland を付けて回すと、新しい branch へ載せ直す")
            return 1
        print(f"STOP: #{pr} で Architecture pipeline が起動していない (validate-level-constraints が checks に無い・main とは衝突しない)。"
              "空の commit を push するか、新しい branch へ載せ直す")
        return 1
    run(["git", "fetch", "-q", "origin", info["headRefName"]])
    head = info["headRefOid"]
    # main は 5 人の merge で数分ごとに動く。確かめている間に動いたら、新しい main に重ね直して回し直す (最大 3 回)
    for attempt in range(1, 4):
        run(["git", "fetch", "-q", "origin", "main"])
        base = run(["git", "rev-parse", "origin/main"]).stdout.strip()
        ok, msg = overlay_check(pr, head, base)
        print(msg)
        if not ok and "--reland" in argv:
            # 数の行だけの衝突なら、新しい branch へ載せ直して新しい PR を出す (merge はしない・50 の依頼)。
            #   衝突しなくても、重ねた形が数の行で赤のこともある (AS-OF の件数が main 側のまま 498 (h) で赤・#3222・2f の依頼)。
            #   reland は載せ直した後に sync_stated_counts --apply を回し、consistency が赤のままなら止まるので、どちらも渡す
            return reland(pr, info)
        if not ok:
            return 1
        if bad_ci:
            print(f"STOP: #{pr} の CI が緑でない (未完了なら終わってから回す): {bad_ci}")
            return 1
        run(["git", "fetch", "-q", "origin", "main"])
        if run(["git", "rev-parse", "origin/main"]).stdout.strip() == base:
            break
        print(f"main が確かめている間に動いた ({attempt} 回目)。重ね直す")
    else:
        print("STOP: main が 3 回続けて動いた。少し待ってから回す")
        return 1
    if dry:
        print("dry-run: merge はしない")
        return 0
    r = run(["gh", "pr", "merge", pr, "--rebase"], check=False)
    state = json.loads(run(["gh", "pr", "view", pr, "--json", "state"]).stdout)["state"]
    if state != "MERGED" and "already in progress" in (r.stdout + r.stderr):
        # 別の人が同じ PR を同時に merge している (2026-11-15・#3139 で 50 と重なった)。少し待って状態を読み直す
        time.sleep(15)
        state = json.loads(run(["gh", "pr", "view", pr, "--json", "state"]).stdout)["state"]
    print(f"{'MERGED' if state == 'MERGED' else 'STOP: merge できなかった'}: #{pr}\n{r.stdout}{r.stderr}".rstrip())
    return 0 if state == "MERGED" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
