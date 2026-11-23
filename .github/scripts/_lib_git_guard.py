"""_lib_git_guard.py — 道具が git の参照を読む前に、`origin/main` が曖昧でないことを確かめる。

**なぜ在るか (2026-11-23・d7 の報告・fc)**: 5 人が同じ repo を worktree で共有するので、誰かが `refs/heads/origin/main`
(ローカル branch) を作ると、全員の `origin/main` がそちらに解決される (git は refs/heads を refs/remotes より先に引く)。
道具は「いまの main」に重ねて照らし、merge し、数を導くので、古い作業 branch を main と取り違えると、#3905 と同じ
「古い base の木で他人の変更を消す」経路になる。同じ日に cd の wip でこの形が起きた。道具の最初で止める。
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def ambiguous_origin_refs(root: Path = ROOT) -> list[str]:
    """`origin` や `origin/...` という名のローカル branch・tag (remote の名と衝突するもの) の一覧。"""
    out = subprocess.run(["git", "for-each-ref", "--format=%(refname)", "refs/heads/origin", "refs/heads/origin/",
                          "refs/tags/origin", "refs/tags/origin/"], cwd=root, text=True, capture_output=True).stdout
    return sorted({ln for ln in out.splitlines() if ln.strip()})


def require_unambiguous_origin(root: Path = ROOT) -> None:
    bad = ambiguous_origin_refs(root)
    if bad:
        print(f"STOP: `origin/main` が曖昧 —— ローカルの参照 {bad} が remote の名と衝突し、`origin/main` が古い作業 branch に "
              "解決される。作った人が `git branch -m <古い名> <新しい名>` で改名してから回す (worktree は参照を共有する)")
        sys.exit(3)
