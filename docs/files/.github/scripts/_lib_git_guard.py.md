---
file: .github/scripts/_lib_git_guard.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-23
canonical-ref: .github/scripts/safe_merge.py (merge の門) / CLAUDE.md §7【5 人体制】(worktree の共有)
---

# .github/scripts/_lib_git_guard.py

## What

道具が git の参照を読む前に、`origin` / `origin/...` という名のローカル branch・tag が無いこと (= `origin/main` が remote の main に解決されること) を確かめる。在れば STOP して改名を促す (終了コード 3)。safe_merge・add_round・add_law_snapshot・record_read・sync_stated_counts・prepare_version_freeze・rehearse_version_freeze・errata_faces・submission_gate の main の最初で呼ぶ。

## Why

2026-11-23、共有の repo に `refs/heads/origin/main` (作業 branch) ができ、全員の `origin/main` がそちらに解決された (git は refs/heads を refs/remotes より先に引く)。道具が古い作業 branch を main と取り違えると、#3905 と同じ「古い base の木で他人の変更を消す」経路になる (d7 の報告)。

## How (usage)

```python
from _lib_git_guard import require_unambiguous_origin
require_unambiguous_origin()
```

## Constraints

worktree は参照を共有するので、1 人が作った branch が全員の道具に効く。止めるだけで、改名は作った人が行う。

## Change impact

git の参照を読む道具を足したら、main の最初でこれを呼ぶ。

## Audience-specific notes

- **全員**: branch を作るときに `origin/` で始まる名を使わない。手で比べるときは `refs/remotes/origin/main` と書くと曖昧にならない。
