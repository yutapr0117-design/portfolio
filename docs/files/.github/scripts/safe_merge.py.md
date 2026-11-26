---
file: .github/scripts/safe_merge.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-26
canonical-ref: CLAUDE.md §5 (AI2AI handoff-first commit/PR discipline・rebase merge) / .github/scripts/check_repository_consistency.py (重ねた形で回す検査)
---

# .github/scripts/safe_merge.py

## What

PR を「いまの main に重ねた形」で consistency check に通してから、`gh pr merge --rebase` する手回しの道具。

1. PR の head と origin/main を取得する。
2. 一時的な worktree（detached）を origin/main に作り、PR の head を merge する。衝突したら止まる。
3. その worktree で `check_repository_consistency.py` を回す。赤なら ERROR の行を出して止まる。
   PR が確定の道具・草案の Check・LICENSES/ の文書（rounds/ を除く）を触るなら、同じ worktree で確定の予行（`rehearse_version_freeze.py`・約 36 秒）も回し、一覧の外で止まれば止まる（2026-11-24 に道具の面、2026-11-26 にドシエの文を足した・議題 36: 468a は「N.M の草案」と引いた逐語を確定の後に本文へ当てるので、文書だけの PR が次の確定を止めうる）。
4. PR の CI が緑で、確かめている間に main が動いていなければ merge する。main が動いていたら新しい main に重ね直して回し直す（最大 3 回）。

`--dry-run` は 4 の merge をしない。worktree は止まった場合も必ず消す。

`--reland`（2026-11-15・50 の依頼）は、3 で衝突したときに、数の行だけの衝突を解いて出し直す。手順は次のとおり。

1. いまの main から `<branch>-reland` を作り、PR の commit を cherry-pick する。
2. 衝突の塊のうち、数だけが違う塊は main 側を採る（後で `sync_stated_counts.py --apply` が実測から書き直す）。両側が行を足しただけの塊（表の行・READ-THREADS の行）は両方を残す。それ以外の塊があれば何もしないで止まる。
3. 載せ直した形で consistency を回し、緑なら push して新しい PR を出し、元の PR を閉じる。merge はしない。新しい PR の CI を待ってから、もう一度 safe_merge で入れる。

同じ日に、50 の指摘で次の 3 点を足した。

- `--reland` の前に、`<branch>-reland` の local / remote の branch と、それを head にする open PR を見る。在れば「既に載せ直し中」と言って止まる（統合役と作者が同時に回すと、2 人目が traceback で落ちた・#3138）。
- merge が「Merge already in progress」で失敗したら、15 秒待って状態を読み直す（#3139 で 50 と重なった）。
- `validate-level-constraints` が checks に無ければ、「Architecture pipeline が起動していない」と言って止まる。trigger の取りこぼしがその日 4 回あり、CodeQL 系だけが緑だと「CI 緑」に見えた。

その日、5 本が rounds/README の在庫・長さの行・AS-OF の件数だけで衝突し、そのたびに手で載せ直した。push 済みの branch は rebase しないので、新しい branch と新しい PR を作る。古い main から runbook の数だけを変えた commit を作り、push と gh を差し替えて、最後まで通ることを確かめた。

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

- **両側が同じ行を書き換えた衝突は止まる（2026-11-16・1c の報告）**: --reland は `merge.conflictStyle=diff3` で cherry-pick し、衝突の塊の元の行（base）を読む。元の行が main 側にも PR 側にも残っていなければ、両側が同じ行を書き換えたので「行を足した」とは扱わず STOP する。T77 の載せ直し（PR 3398）では、30 が PR 3396 で直した submission-osd の OSD 5 と §11.3 の行が、PR 側の古い理由の行と並んで残り、古い形が戻った。直した道具で同じ cherry-pick を再生すると STOP する（旧版は「解いた」）。数だけの違い・path の行（main 側）・元の行の無い追加は従来どおり解く。
