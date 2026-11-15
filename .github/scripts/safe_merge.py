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
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(cmd: list[str], cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=check)


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
    run(["git", "fetch", "-q", "origin", info["headRefName"]])
    head = info["headRefOid"]
    # main は 5 人の merge で数分ごとに動く。確かめている間に動いたら、新しい main に重ね直して回し直す (最大 3 回)
    for attempt in range(1, 4):
        run(["git", "fetch", "-q", "origin", "main"])
        base = run(["git", "rev-parse", "origin/main"]).stdout.strip()
        ok, msg = overlay_check(pr, head, base)
        print(msg)
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
    print(f"{'MERGED' if state == 'MERGED' else 'STOP: merge できなかった'}: #{pr}\n{r.stdout}{r.stderr}".rstrip())
    return 0 if state == "MERGED" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
