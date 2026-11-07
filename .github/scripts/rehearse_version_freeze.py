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
EXPECTED = {"91", "121", "362", "444m", "460", "468", "472c", "472h"}


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, text=True, capture_output=True).stdout


def rehearse(tree: Path) -> list[str]:
    tool = subprocess.run([sys.executable, ".github/scripts/prepare_version_freeze.py", "--date", datetime.date.today().isoformat()],
                          cwd=tree, text=True, capture_output=True)
    if tool.returncode != 0:
        return [f"確定の道具が止まった: {(tool.stderr or tool.stdout)[-300:]}"]
    git("add", "--", *git("ls-files", "--others", "--exclude-standard", cwd=tree).split(), cwd=tree)
    check = subprocess.run([sys.executable, ".github/scripts/check_repository_consistency.py"], cwd=tree, text=True, capture_output=True)
    out = check.stdout + check.stderr
    if "Traceback" in out:
        return [f"consistency が traceback で止まった: {out[-300:]}"]
    red = {m.group(1) for m in re.finditer(r"^ERROR: Check (\S+?):", out, re.M)}
    print(f"確定の直後の RED: {sorted(red)}")
    return [f"一覧の外の RED: Check {n}" for n in sorted(red - EXPECTED)]


def main() -> int:
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
