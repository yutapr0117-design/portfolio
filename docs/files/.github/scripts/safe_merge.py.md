---
file: .github/scripts/safe_merge.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-15
canonical-ref: CLAUDE.md §5 (AI2AI handoff-first commit/PR discipline・rebase merge) / .github/scripts/check_repository_consistency.py (重ねた形で回す検査)
---

# .github/scripts/safe_merge.py

## What

PR を「いまの main に重ねた形」で consistency check に通してから、`gh pr merge --rebase` する手回しの道具。

1. PR の head と origin/main を取得する。
2. 一時的な worktree（detached）を origin/main に作り、PR の head を merge する。衝突したら止まる。
3. その worktree で `check_repository_consistency.py` を回す。赤なら ERROR の行を出して止まる。
4. PR の CI が緑で、確かめている間に main が動いていなければ merge する。main が動いていたら新しい main に重ね直して回し直す（最大 3 回）。

`--dry-run` は 4 の merge をしない。worktree は止まった場合も必ず消す。

## Why

2026-11-15、5 人が並行して PR を merge していた。rounds/ に受領文を足す 2 本は、どちらも README の在庫見出しを「444」にしてそれぞれ緑で merge された。その結果 main の Check 465 が 444 / 445 で赤になり、その後に出た無関係な PR（#3060）の CI まで落ちた。PR の CI は PR を出した時点の main と重ねて回るので、merge の直前の main とは重ねていない。

## How (usage)

```bash
python3 .github/scripts/safe_merge.py 3060            # 確かめて merge する
python3 .github/scripts/safe_merge.py 3060 --dry-run  # 確かめるだけ
```

## Constraints

- 回すのは consistency だけで、verify の全段（lint・e2e）は回さない。並行の merge で壊れるのは、数と参照の照合だからである。e2e は PR の CI が見る。
- force-push、rebase した branch の push、auto merge はしない。衝突したら、新しい branch へ cherry-pick して出し直す（PR branch へ main を merge しない規律と同じ）。
- 1 回の確認に 1〜2 分かかる。その間に main が 3 回続けて動いたら止まる。

## Change impact

- `check_repository_consistency.py` の出力の形（`ERROR:` で始まる行）を変えると、赤の判定と表示が変わる。

## Audience-specific notes

### For AI agents（次担当）

- 他のセッションの PR が多い時間帯は、`gh pr merge` を直接呼ばずにこれを使う。

### For human engineers（新卒レベル）

「この PR を今の main に入れたら検査が通るか」を、一時的な作業コピーで試してから取り込む道具。

### For third parties / auditors

merge の直前の main との組み合わせを検査した記録は、出力の `OK: #N (head) をいまの main (base) に重ねて consistency は緑` の行に残る。
