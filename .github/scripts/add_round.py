#!/usr/bin/env python3
"""add_round.py — 公開アーカイブの月の写しから通を切り出し、LICENSES/rounds/ に受領文を 1 ファイル置く一式。

**なぜ在るか (2026-11-15・2f の依頼)**: 2f は受領文を 1 日に 15 回ほど手で置き、2 回ずれた。件名の折り返し
(`Subject: … reinvention\\n dilemma`) で照合が外れ、Date の先頭の空白 (" 2 Sep") でも外れた。一式は 5 段で、どれも
機械にできる: (1) 通の切り出しとヘッダ、(2) 行数の止め (1,000 行で止め・800 行で警告)、(3) docs/files の mirror の雛形、
(4) rounds/ の在庫表 (年の帯ごとの分冊 INVENTORY-*.md) へ日付の位置で 1 行差し込む、(5) runbook §9 の数 (sync_stated_counts.py が実測から書き直す)。

**切り出し**: pipermail の月の写しを `From <addr>  <曜日> <月> …` の区切りで通に分け、件名は折り返しをつないでから
`[License-discuss]` / `Re:` を外して照らす。Date は空白を 1 つにつぶしてから部分一致で照らす。通の本文は 1 byte も
変えずにそのまま書く (`----- begin verbatim -----` より下は無改変・rounds/README の規約)。

**書くもの**: `LICENSES/rounds/<YYYY-MM>-<list>-<slug>-observed.txt` (既に在れば止まる)、mirror doc、在庫表 (分冊) の 1 行。
最後に git add して `sync_stated_counts.py --apply` を回す (runbook §9 の追跡ファイルの数)。--dry-run は何も書かない。

使い方:
    python3 .github/scripts/add_round.py --list license-discuss --month 2024-March \\
        --subject "Blue OakModel License and the license reinvention" --sender "Bruce Perens" --count 1 \\
        --slug blue-oak-reinvention --position "Not addressed to us. Observed. The message is kept whole." \\
        --what "…から … 氏の 1 通を無改変で置いた。…" --why "`ACD-1.0.review-readings.md` §1.217 の一次資料として置く。" \\
        --row "**観測（…から 1 通・…）**" [--date "15 Mar 2024"] [--dry-run]
環境変数 DOSSIER_ARCHIVE_CACHE (既定 ~/osi-archive-cache) に月の写しを置く。
"""
from __future__ import annotations

import argparse
import datetime
import email.header
import email.utils
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROUNDS = ROOT / "LICENSES" / "rounds"
SEP = re.compile(r"^From \S+ at \S+\s+\w{3} \w{3}\s+\d+ \d\d:\d\d:\d\d \d{4}\s*$", re.M)
MONTHS = "January February March April May June July August September October November December".split()


def messages(text: str) -> list[str]:
    starts = [m.start() for m in SEP.finditer(text)]
    return [text[a:b] for a, b in zip(starts, starts[1:] + [len(text)])]


def header(msg: str, name: str) -> str:
    head = msg.split("\n\n", 1)[0]
    m = re.search(rf"^{name}: (.*(?:\n[ \t].*)*)", head, re.M)
    return " ".join(m.group(1).split()) if m else ""


def subject_core(s: str) -> str:
    # MIME 符号化の件名 (=?utf-8?q?…?=) を復号してから照らす (2f の落とし穴 (4))
    try:
        s = str(email.header.make_header(email.header.decode_header(s)))
    except Exception:  # noqa: BLE001 —— 復号できない件名はそのまま照らす
        pass
    # 外すのはリストの札 ([License-discuss] / [License-review]) だけ。角括弧の中身を全部消すと、
    #   "resolving ambiguities in OSD [was Re: For Approval: License Zero Reciprocal …]" の [was Re: …] まで消え、
    #   元の件名で探せなかった (2026-11-15・2f の観測・Phipps 2017-10-25)
    s = re.sub(r"\[License-[^\]]*\]", "", s, flags=re.I)
    while True:
        t = re.sub(r"^\s*(?:re|fwd?|aw)\s*:\s*", "", s, flags=re.I)
        if t == s:
            return " ".join(s.split())
        s = t


def date_matches(msg: str, day, hhmm) -> bool:
    """--date の 1 つ (日付と、あれば時刻) が、この通の Date 見出しに合うか。時刻は見出しの現地時刻で比べる。"""
    if msg_date(msg) != day:
        return False
    if hhmm is None:
        return True
    try:
        return email.utils.parsedate_to_datetime(header(msg, "Date")).strftime("%H:%M:%S" if hhmm.count(":") == 2 else "%H:%M") == hhmm
    except (TypeError, ValueError):
        return False


def msg_date(msg: str):
    """通の Date を日付に (読めなければ None)。"""
    try:
        return email.utils.parsedate_to_datetime(header(msg, "Date")).date()
    except (TypeError, ValueError, IndexError):
        return None


def own(msg: str) -> str:
    """引用行 (>) を除いた本文を空白で正規化したもの (本文の決め手 --needle を当てる先・2f の落とし穴 (3))。"""
    body = msg.split("\n\n", 1)[1] if "\n\n" in msg else ""
    return " ".join(" ".join(ln for ln in body.splitlines() if not ln.startswith(">")).split())


def main(argv: list[str]) -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _lib_git_guard import require_unambiguous_origin
    require_unambiguous_origin()  # origin/main が古い作業 branch に解決されないこと (2026-11-23)
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    for a in ("list", "slug", "position", "what", "why", "row"):
        ap.add_argument(f"--{a}", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--subject", help="件名の一部 (文字どおり・空白の違いは無視)。'BSD + Patent' や 'C++' もそのまま書く")
    g.add_argument("--subject-regex", help="件名の正規表現 (要るときだけ)")
    ap.add_argument("--count", type=int, help="選ばれる通の数。違えば止まる (同じ人・同じ日に複数の通がある会話で取り違えない)")
    ap.add_argument("--month", action="append", required=True, help="2024-March の形。会話が月をまたぐなら複数 (2f の落とし穴 (6))")
    ap.add_argument("--sender", action="append", default=[])
    ap.add_argument("--date", action="append", default=[])
    ap.add_argument("--needle", action="append", default=[], help="本文の決め手 (引用行を除いた本文の部分一致)")
    ap.add_argument("--dry-run", action="store_true")
    o = ap.parse_args(argv)
    cache = Path(os.environ.get("DOSSIER_ARCHIVE_CACHE", Path.home() / "osi-archive-cache"))
    srcs = [cache / f"{o.list}-{m}.txt" for m in o.month]
    missing = [str(s) for s in srcs if not s.exists()]
    if missing:
        print(f"STOP: 月の写しが無い: {missing}")
        return 1
    year, mon = o.month[0].split("-")
    mm = f"{year}-{MONTHS.index(mon) + 1:02d}"
    out = ROUNDS / f"{mm}-{o.list}-{o.slug}-observed.txt"
    if out.exists():
        print(f"STOP: 既に在る: {out.relative_to(ROOT)}")
        return 1
    # 件名は既定で文字どおりに照らす (2026-11-15・2f の検証: "BSD + Patent" を正規表現として読み 0 通で止まった)
    rx = re.compile(o.subject_regex if o.subject_regex else r"\s+".join(re.escape(w) for w in o.subject.split()), re.I)
    want_dates = set()  # (日付, 時刻 or None)。時刻つきは Date 見出しの現地時刻と秒まで (分までなら分まで) 比べる
    for d in o.date:  # Date は日付として比べる ("2 Sep 2015" の部分一致は "12 Sep 2015" にも当たった・2f の検証)
        # 時刻つき ("16 Mar 2008 13:57:10") も読む (2026-11-23・d7: 同じ日に同じ人の通が複数ある会話で止まった)
        for fmt in ("%d %b %Y", "%Y-%m-%d", "%d %B %Y", "%d %b %Y %H:%M:%S", "%d %b %Y %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
            try:
                _dt = datetime.datetime.strptime(" ".join(d.split()), fmt)
                want_dates.add((_dt.date(), _dt.strftime("%H:%M:%S" if fmt.endswith("%S") else "%H:%M") if "%H" in fmt else None))
                break
            except ValueError:
                continue
        else:
            print(f"STOP: --date を日付として読めない: {d!r} (例: '2 Sep 2015' / 2015-09-02 / '16 Mar 2008 13:57:10')")
            return 1
    thread = [m for s in srcs for m in messages(s.read_text(encoding="utf-8", errors="surrogateescape"))
              if rx.search(subject_core(header(m, "Subject")))]
    picked = [m for m in thread
              if (not o.sender or any(s.lower() in header(m, "From").lower() for s in o.sender))
              and (not want_dates or any(date_matches(m, d, tm) for d, tm in want_dates))
              and (not o.needle or any(n in own(m) for n in o.needle))]
    if not picked:
        print(f"STOP: 一致する通が無い (件名に一致 {len(thread)} 通・差出人・日付・本文の決め手で 0 通)")
        return 1
    if o.count is not None and len(picked) != o.count:
        print(f"STOP: 選ばれた通が {len(picked)} 通で --count {o.count} と違う。--needle / --date / --sender で絞る "
              "(同じ日に同じ人の通が複数あるなら、--needle に本文の決め手を渡すか、--date に下の時刻まで渡す):")
        for m in picked:
            print(f"  {header(m, 'Date')} | {header(m, 'From')} | {own(m)[:80]}")
        return 1
    src = srcs[0]
    first = email.utils.parsedate_to_datetime(header(thread[0], "Date")).date().isoformat()
    senders = []
    for m in picked:
        name = re.sub(r"^.*\((.*)\)\s*$", r"\1", header(m, "From"))
        if name not in senders:
            senders.append(name)
    retrieved = datetime.date.fromtimestamp(src.stat().st_mtime).isoformat()
    today = datetime.date.today().isoformat()
    title = subject_core(header(thread[0], "Subject"))
    body = "".join(picked)
    text = (f"Source: OSI {o.list} public archive, {', '.join(m + '.txt' for m in o.month)}\n"
            f"Retrieved: {retrieved} (local copy of the public archive; read {today})\n"
            f"Messages: {len(picked)} of {len(thread)} in \"{title}\" ({first})\n"
            f"Senders: {', '.join(senders)}\n"
            f"Position: {o.position}\n\n----- begin verbatim -----\n" + body.rstrip("\n") + "\n")
    lines = text.count("\n")
    if lines > 1000:
        print(f"STOP: {lines} 行で 1,000 行 (Check 365) を越える。--sender / --date で通を絞るか、2 分割して置く")
        return 1
    if lines > 800:
        print(f"警告: {lines} 行で 800 行 (早期警告) を越える")
    rel = out.relative_to(ROOT)
    mirror = ROOT / "docs" / "files" / f"{rel}.md"
    doc = (f"---\nfile: {rel}\naudience: ai, human (新卒), 監査人, 第三者全般\nlast-updated: {today}\n"
           f"canonical-ref: LICENSES/rounds/README.md (置き方の規約)\n---\n\n# {rel}\n\n## What\n\n{o.what}\n\n## Why\n\n{o.why}\n\n"
           f"## How\n\n公開アーカイブのローカルの写しから {today} に切り出した（`add_round.py`）。先頭に最小限のヘッダを足し、"
           "`----- begin verbatim -----` より下は無改変である。\n\n## Constraints\n\n無改変保存の場所なので本文を直さない"
           "（`rounds/README.md`）。\n\n## Change impact\n\nこのファイルの通を引く節を直すときは、引用が本文に在るかを確かめる。\n\n"
           "## Audience-specific notes\n\n- **監査人**: 引用は元のアーカイブの月に当てて確かめられる。\n")
    # 在庫表は年の帯ごとの分冊 (2026-11-23・README が 800 行を越えた)。差し込みの規則は _lib_rounds_inventory が 1 つだけ持つ
    from _lib_rounds_inventory import insert_row
    row = f"| {mm} | `{o.list}` | {o.row} | `{out.name}` |"
    inv, at_line = insert_row(ROUNDS, mm, row, date_re=r"\d{4}-\d{2}", write=False)
    print(f"{rel}: {len(picked)} 通 / 件名に一致 {len(thread)} 通・{lines} 行・差出人 {', '.join(senders)}")
    print(f"在庫表 ({inv.name}): {row[:100]}… を {at_line} 行目の後へ")
    if o.dry_run:
        print("dry-run: 何も書かない")
        return 0
    out.write_text(text, encoding="utf-8", errors="surrogateescape")
    mirror.write_text(doc, encoding="utf-8")
    insert_row(ROUNDS, mm, row, date_re=r"\d{4}-\d{2}")
    subprocess.run(["git", "add", str(out), str(mirror)], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT / ".github/scripts/sync_stated_counts.py"), "--apply"], cwd=ROOT)
    print("書いた。引く節に §・逐語を書き、verify を回す")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
