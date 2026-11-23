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
    python3 .github/scripts/safe_merge.py 3060 --allow-revert  # main の最近の commit を巻き戻す PR を、意図した revert として通す

**--reland (2026-11-15・50 の依頼)**: 同じ日に 5 本が「main 側も動かした数の行」(rounds/README の在庫・長さの行・AS-OF の
件数) だけで衝突し、そのたびに手で載せ直した。--reland は、いまの main から `<branch>-reland` を作って PR の commit を
cherry-pick し、衝突の塊を次の 2 つに限って解く: 数だけが違う塊 (main 側を採り、後で sync_stated_counts.py --apply が
実測から書き直す) と、両側が行を足しただけの塊 (表の行・READ-THREADS の行・mutation の append-log の末尾 (2026-11-23)。両方を残す)。それ以外の塊があれば何も
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
        # 確定の道具と、確定の直後に効く面を触る PR は、確定の予行も重ねた形で回す (2026-11-24・fc): 予行は週次 (mutation-probe.yml)
        #   でしか回らず、#3922 (道具が空の「## 記述子の候補」を置く) と #3932 (468z がその節を読む) は、それぞれ緑で入ったのに
        #   組み合わせで次の確定を止めていた (#4000 で直した)。予行は 30 秒ほどかかるので、触った file で絞る
        changed = [f for f in run(["git", "diff", "-z", "--name-only", f"{base}...{head}"], check=False).stdout.split("\0") if f]
        if any(REHEARSE_TRIGGER.search(f) for f in changed):
            r = run([sys.executable, ".github/scripts/rehearse_version_freeze.py"], cwd=wt, check=False)
            if r.returncode:
                tail = [ln for ln in (r.stdout + r.stderr).splitlines() if ln.startswith(("ERROR", "確定の直後"))]
                return False, (f"STOP: #{pr} をいまの main ({base[:8]}) に重ねると、確定の予行が一覧の外で止まる (次の確定を止める):\n"
                               + "\n".join(tail[-4:]))
            return True, f"OK: #{pr} ({head[:8]}) をいまの main ({base[:8]}) に重ねて consistency は緑・確定の予行も通る"
        return True, f"OK: #{pr} ({head[:8]}) をいまの main ({base[:8]}) に重ねて consistency は緑"
    finally:
        run(["git", "worktree", "remove", "--force", str(wt)], check=False)
        shutil.rmtree(tmp, ignore_errors=True)


# 確定の予行を重ねて回す PR の file (確定の道具・草案の Check・CHANGELIST の雛形を読む面・mutation の版の組み立て)
REHEARSE_TRIGGER = re.compile(r"^\.github/scripts/(?:prepare_version_freeze|rehearse_version_freeze|checks_license_draft|_lib_draft_\w+"
                              r"|checks_license_stated_counts|mutation_samples_common|make_redline)\.py$")


# diff3 の形 (`||||||| base` の節) も読む。base は両側が書き換えた元の行で、reland は merge.conflictStyle=diff3 で cherry-pick する
_HUNK = re.compile(r"^<<<<<<< [^\n]*\n(.*?)(?:^\|\|\|\|\|\|\| [^\n]*\n(.*?))?^=======\n(.*?)^>>>>>>> [^\n]*\n", re.M | re.S)


_ASOF_ROW = "| **未読スレッドの残り** |"
_RECENT = re.compile(r"（直近の 1 件: (.*?)(?:）。|。）) \*\*それより前の")  # 閉じ方の両方を読む (record_read と同じ)
MOVED_RECENT: list[str] = []  # AS-OF の行の衝突で main 側を採ったとき、PR 側の「直近の 1 件」(LOG へ移す)


# mutation の append-log の行 (dict の entry の本文・閉じ・開き・コメント)
_APPEND_LINE = re.compile(r'^(?:\s+(?:"|#|[A-Za-z_(\]\[f\'])|\}\)\s*$|_\w+_TAIL\.append\(\{\s*$)')
_TAIL_OPEN = re.compile(r"^(_\w+_TAIL\.append\(\{)\s*$", re.M)


def resolve_numbers_only(text: str) -> tuple[str | None, list[str]]:
    """衝突の塊を、数だけが違う塊 (main 側を採る) と、両側が行を足しただけの塊 (両方を残す) に限って解く。

    返り値: (解いた本文 か 解けなければ None, 解けなかった塊の頭)。数は後で sync_stated_counts.py --apply が実測から
    書き直すので、main 側の数を採ってよい。行を足しただけの塊は在庫表の行・READ-THREADS の行の形で、順は main → PR。
    """
    bad = []

    def fix(m):
        ours, base, theirs = m.group(1), m.group(2) or "", m.group(3)  # cherry-pick では ours = main 側 (HEAD)、theirs = PR の commit
        # 両側が同じ元の行を書き換えた (元の行がどちらにも残っていない) のは「行を足した」ではない (2026-11-16・1c の報告):
        #   T77 の載せ直し (#3398) で、30 が #3396 で直した submission-osd の OSD 5 の行と、PR が同じ行を古い理由のまま
        #   書き換えた行が「表の行を足しただけ」として両方残り、古い形が戻った。数だけの違いと path の行 (main 側を採る) は従来どおり
        _both = [ln for ln in base.splitlines(keepends=True) if ln.strip() and ln not in ours and ln not in theirs]
        if re.sub(r"\d", "0", ours) == re.sub(r"\d", "0", theirs):
            return ours
        if not ours.strip() or not theirs.strip():
            return ours + theirs
        o, t = ours.splitlines(keepends=True), theirs.splitlines(keepends=True)
        # mutation の append-log の末尾 (2026-11-23・6d の依頼・fc): 5 人が同じ末尾に `_MUTATIONS_TAIL.append({…})` を 1 つずつ
        #   足すので、両側の entry の本文が同じ append の中で衝突する。両方を別々の append として残す (main → PR の順)。
        #   1 つの dict に融合させると片方の key が黙って消える (Check 480 の形) ので、間で閉じて開き直す
        if not _both and all(_APPEND_LINE.match(ln) for ln in o + t if ln.strip()):
            tail = _TAIL_OPEN.findall(text[:m.start()])
            if tail and not ours.rstrip().endswith("})") and not theirs.lstrip().startswith(tail[-1]):
                return ours + "})\n" + tail[-1] + "\n" + theirs
            if ours.rstrip().endswith("})") or theirs.lstrip().startswith(("_MUTATIONS_TAIL.append({", "_E2E_TAIL.append({")):
                return ours + theirs
        # AS-OF の「未読スレッドの残り」の行 (2026-11-15・50 の依頼): 5 人の record_read が毎回この 1 行を書き換える。
        #   main 側を採り、PR 側の「直近の 1 件」は LOG の先頭へ移す (reland が書く)。件数は sync_stated_counts が
        #   READ-THREADS と THREAD-CANDIDATES から導き直す (498 (h) と同じ数え方)
        if len(o) == len(t) == 1 and o[0].startswith(_ASOF_ROW) and t[0].startswith(_ASOF_ROW):
            mo, mt = _RECENT.search(o[0]), _RECENT.search(t[0])
            if mt and (not mo or mo.group(1) != mt.group(1)):
                MOVED_RECENT.append(mt.group(1))
            return ours
        if all(ln.startswith("|") for ln in o + t):
            # 表の行は、先頭のセル (path や番号) が main 側に在る行を足さない —— 同じ path の行を両側とも残すと、予算表 (§2) に
            #   同じ file の行が 2 つ並び Check 424c で止まった (2026-11-16・50 の報告・#3369 と #3372)。数は sync が実測から直す
            #   先頭のセルで同じ行と見なすのは、セルが path か番号のとき (予算表・反映の表) だけ。rounds/README の在庫表のように
            #   先頭が月 (「2002-10」) の表は、別の受領文の行まで落とすので、行全体で比べる
            def key(ln):
                c = ln.split("|")[1].strip() if ln.count("|") >= 2 else ln
                return c if re.fullmatch(r"`?[\w./\-]+/[\w./\-]+`?|`?[\w.\-]+\.(?:md|txt|py|js|json|yml)`?(?: \d+\.\d+)?|\d+(?:\.\d+)?", c) else ln
            have = {key(ln) for ln in o}
            _rest = [ln for ln in t if ln not in o and key(ln) not in have]
            if _both and any(key(ln) == ln for ln in _rest):  # path でない行を両側が書き換えた
                bad.append("両側が同じ表の行を書き換えた: " + _both[0][:70])
                return m.group(0)
            return ours + "".join(_rest)
        if all(re.match(r"\d{4}-\d{2}-\d{2}\t", ln) for ln in o + t):
            return ours + "".join(ln for ln in t if ln not in o)
        # READ-THREADS-LOG の先頭の項目 (`- …` と空行): 5 人が同じ位置に 1 項目ずつ挿す。両方を残す (main → PR の順)
        if all(ln.startswith("- ") or not ln.strip() for ln in o + t) and not _both:
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
            r = run(["git", "-c", "merge.conflictStyle=diff3", "cherry-pick", c], cwd=wt, check=False)
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
            run([sys.executable, ".github/scripts/sync_size_table.py"], cwd=wt, check=False)  # 予算表の実測の行数
            run(["git", "add", "-u"], cwd=wt)
            if run(["git", "diff", "--cached", "--quiet"], cwd=wt, check=False).returncode == 0:
                # 件数だけの commit は、main 側を採って sync で導き直すと変更が残らない。--continue は "nothing to commit" で
                #   落ちる (2026-11-15・50 が #3244 で再現)。sync が同じ数を導くので、その commit は落としてよい
                run(["git", "cherry-pick", "--skip"], cwd=wt)
                continue
            run(["git", "-c", "core.editor=true", "cherry-pick", "--continue"], cwd=wt)
        run([sys.executable, ".github/scripts/sync_stated_counts.py", "--apply"], cwd=wt, check=False)
        # 予算表の行数も最後に揃える (2026-11-19 #3683: 衝突の無い載せ直しでは上のループの sync_size_table が走らず、PR と main の両方が
        #   UNIQUE-READING に行を足すと Check 424 の表の行数だけがずれて STOP した)。どちらの sync が書き換えたかは diff で見る
        run([sys.executable, ".github/scripts/sync_size_table.py"], cwd=wt, check=False)
        run(["git", "add", "-u"], cwd=wt)
        if run(["git", "diff", "--cached", "--quiet"], cwd=wt, check=False).returncode != 0:
            run(["git", "commit", "-q", "-m", "chore: 載せ直しの後に、実測から導ける数と予算表の行数を sync_stated_counts.py --apply と "
                 "sync_size_table.py で書き直す"], cwd=wt)
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


def _diff_lines(rng: list[str], files: list[str] | None = None) -> dict[str, tuple[set[str], set[str]]]:
    """git diff の範囲を file ごとの (足した行, 消した行) に。短い行 (10 字未満・括弧だけ等) は重なりの数に入れない。"""
    out: dict[str, tuple[set[str], set[str]]] = {}
    cur = None
    for ln in run(["git", "-c", "core.quotepath=off", "diff", "--no-color", "-U0", *rng, "--", *(files or [])]).stdout.splitlines():
        if ln.startswith("+++ "):
            cur = ln[6:] if ln.startswith("+++ b/") else None
            if cur:
                out.setdefault(cur, (set(), set()))
        elif cur and ln[:1] in "+-" and not ln.startswith(("+++", "---")) and len(ln[1:].strip()) >= 10:
            out[cur][0 if ln[0] == "+" else 1].add(ln[1:].strip())
    return out


def revert_check(head: str, base: str, days: int = 4) -> list[str]:
    """PR が main の最近の commit を巻き戻していないか (2026-11-23・6d の依頼・fc)。

    d7 の #3905 (9171a4b2) は、古い file の写しを commit して、同じ日に main へ入った #3902 / #3903 ほか 5 本の行を消し、古い形を
    戻した。consistency は「古いが整合した状態」なので緑のまま通り、safe_merge も気づかなかった。PR の commit の親には消された
    行が在ったので、merge-base より後の commit だけを見ても捕まらない。そこで、PR の diff (merge-base..head) が消す行と、main の
    最近 days 日の commit (PR 自身の commit を件名で除く) が足した行を file ごとに比べ、ある commit の足した行 (3 行以上) の
    半分以上を消し (PR が別の場所へ足し直した行は移したので除く)、かつその commit が消した行 (3 行以上) の半分以上を足し戻して
    いる (古い形の復元) なら、その commit を巻き戻していると読む。
    返り値は見つけた巻き戻しの文の list (空なら無い)。意図した revert は main() の --allow-revert で通す。
    """
    mb = run(["git", "merge-base", base, head]).stdout.strip()
    pr_diff = _diff_lines([mb, head])
    if not pr_diff:
        return []
    own = {s for s in run(["git", "log", "--format=%s", f"{mb}..{head}"]).stdout.splitlines()}
    # 移した行 (同じ PR が別の file か同じ file の別の場所に足し直した行) は消したと数えない —— 在庫表の分冊・確定の付録への写し
    moved = set().union(*(a for a, _r in pr_diff.values()))
    since = f"{days} days ago"
    found = []
    for c in run(["git", "log", "--format=%H%x09%ct%x09%s", f"--since={since}", base, "--", *pr_diff]).stdout.splitlines():
        sha, _ct, subj = c.split("\t", 2)
        if subj in own:
            continue
        # 「消して、しかも古い行を戻す」だけを数える (2026-11-23 に main の 150 commit で測った): 「24 時間以内の commit の行を消す」も
        #   条件にすると、同じ日の書き直し (試作の節番号の付け直し・T の追い書き) で 13 件当たった。この形では今日の #3905 の 1 件だけ
        for f, (ca, cr) in _diff_lines([f"{sha}^", sha], list(pr_diff)).items():
            if f not in pr_diff or len(ca) < 3:
                continue
            pa, pr_rm = pr_diff[f]
            lost = (ca & pr_rm) - moved
            gone = len(lost) / len(ca)
            restored = len(cr) >= 3 and len(cr & pa) / len(cr) >= 0.5
            if gone >= 0.5 and restored:
                found.append(f"{sha[:8]} ({subj[:50]}) の {f}: 足した {len(ca)} 行のうち {len(lost)} 行を消し、"
                             f"消した {len(cr)} 行のうち {len(cr & pa)} 行を戻す")
    return found


def main(argv: list[str]) -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _lib_git_guard import require_unambiguous_origin
    require_unambiguous_origin()  # origin/main が古い作業 branch に解決されないこと (2026-11-23)
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
    # PR の head が origin の branch の先頭に追いついているか (2026-11-20 #3735: 9b が 2 つ目の commit を push した後、GitHub の PR の
    #   head が数分古いまま残り、その間に merge が走って 2 つ目の commit が main に入らなかった)。確かめるのは古い head の CI と
    #   consistency なので、追いつくまで merge しない。merge にも --match-head-commit で同じ SHA を渡し、間に push されても止まる
    remote = run(["git", "ls-remote", "origin", f"refs/heads/{info['headRefName']}"]).stdout.split()
    if remote and remote[0] != head:
        print(f"STOP: #{pr} の PR の head ({head[:8]}) が origin の {info['headRefName']} の先頭 ({remote[0][:8]}) に追いついていない —— "
              "push の直後は GitHub の更新を待ってから回す (古い head の CI で merge しない)")
        return 1
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
    reverted = revert_check(head, base)
    if reverted and "--allow-revert" not in argv:
        print(f"STOP: #{pr} は main の最近の commit を巻き戻している (古い file の写しを commit した形・2026-11-23 の #3905):\n  "
              + "\n  ".join(reverted[:6]) + "\n意図した revert なら --allow-revert を付けて回す。そうでなければ、その file を "
              "いまの main から取り直して自分の変更だけを当て直す")
        return 1
    if dry:
        print("dry-run: merge はしない")
        return 0
    r = run(["gh", "pr", "merge", pr, "--rebase", "--match-head-commit", head], check=False)
    state = json.loads(run(["gh", "pr", "view", pr, "--json", "state"]).stdout)["state"]
    if state != "MERGED" and "already in progress" in (r.stdout + r.stderr):
        # 別の人が同じ PR を同時に merge している (2026-11-15・#3139 で 50 と重なった)。少し待って状態を読み直す
        time.sleep(15)
        state = json.loads(run(["gh", "pr", "view", pr, "--json", "state"]).stdout)["state"]
    print(f"{'MERGED' if state == 'MERGED' else 'STOP: merge できなかった'}: #{pr}\n{r.stdout}{r.stderr}".rstrip())
    return 0 if state == "MERGED" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
