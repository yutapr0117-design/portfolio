#!/usr/bin/env python3
"""ドシエが引く発言のうち、同じ差出人が後で取り消した可能性があるものを洗い出す (手で回す道具・CI には入れない)。

    DOSSIER_ARCHIVE_CACHE=<月次アーカイブの場所> python3 .github/scripts/find_quote_retractions.py

2026-11-06 に、不利な事実として 2 か月数えていた Piana 氏の発言を本人が同じ日に撤回していたと分かった。
掃引は "OSI requires" の語で探していたので、撤回の文を拾えなかった。ここは逆から探す。逐語引用をアーカイブの
メッセージへ解決し、同じ差出人の同じスレッドの後続メッセージに撤回の語があるものを出す。

出すのは候補である。撤回かどうかは人が読んで決める。**出なかったことは撤回が無かった証拠ではない**: アーカイブに
解決できない引用と、語の一覧に無い言い方は見ていない。解決できなかった件数も必ず出す。
"""
from __future__ import annotations

import datetime
import email.utils
import glob
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_dossier_quotations import collect_quotes, norm  # noqa: E402

if sys.version_info < (3, 10):
    sys.exit("Python 3.10 or later is required")

CACHE = os.environ.get("DOSSIER_ARCHIVE_CACHE", str(Path.home() / "osi-archive-cache"))
WINDOW_DAYS = 45
RETRACT = re.compile(
    r"stand corrected|i was wrong|i(?:'m| am) wrong|i withdraw|i retract|(?:bad|poor) choice of words|"
    r"my mistake|my error|my bad|i misspoke|i misread|i misunderstood|i take (?:that|it) back|"
    r"i was mistaken|that was wrong|should have said|scratch that|mea culpa|correct myself|"
    r"correction to my|i was incorrect|i got that wrong|ignore my", re.I)
SPLIT = re.compile(r"^From \S+ at \S+\s+\w{3} \w{3}\s+\d+ [\d:]+ \d{4}$", re.M)


def header(raw: str, name: str) -> str:
    m = re.search(rf"^{name}: (.*(?:\n[ \t].*)*)", raw, re.M)
    return " ".join(m.group(1).split()) if m else ""


def thread(subject: str) -> str:
    s = re.sub(r"\[[^\]]*\]", " ", subject)
    s = re.sub(r"(?i)\b(re|fwd?):", " ", s)
    return " ".join(s.lower().split())


def load() -> list[dict]:
    messages = []
    for path in sorted(glob.glob(os.path.join(CACHE, "*.txt"))):
        text = Path(path).read_text(encoding="utf-8", errors="replace")
        marks = [m.start() for m in SPLIT.finditer(text)] + [len(text)]
        for a, b in zip(marks, marks[1:]):
            raw = text[a:b]
            head, _, body = raw.partition("\n\n")
            try:
                when = email.utils.parsedate_to_datetime(header(head, "Date"))
                when = when.replace(tzinfo=None) if when else None
            except (TypeError, ValueError):
                when = None
            own = "\n".join(l for l in body.splitlines() if not l.lstrip().startswith(">"))
            messages.append({"sender": header(head, "From").split("(")[0].strip().lower(),
                             "name": (re.search(r"\((.*)\)", header(head, "From")) or [None, "?"])[1],
                             "when": when, "thread": thread(header(head, "Subject")),
                             "subject": header(head, "Subject"), "file": os.path.basename(path),
                             "own": own, "n": norm(own)})
    return messages


def main() -> int:
    messages = load()
    if not messages:
        print(f"No archive messages in {CACHE}. Set DOSSIER_ARCHIVE_CACHE.")
        return 2
    print(f"# messages {len(messages)} from {CACHE}")
    by_thread: dict[str, list[dict]] = {}
    for m in messages:
        by_thread.setdefault(m["thread"], []).append(m)
    quotes = collect_quotes(".")
    resolved, unresolved, hits, seen = 0, 0, 0, set()
    for q, places in quotes.items():
        where = ", ".join(sorted(places)[:3])
        # 省略記号を挟む引用は最も長い断片で探す。全文では見つからない。
        nq = max((norm(x) for x in re.split(r"\.{3}|…|\[[^\]]*\]", q)), key=len)
        if len(nq.split()) < 5:
            continue
        src = [m for m in messages if nq in m["n"]]
        if not src:
            unresolved += 1
            continue
        resolved += 1
        m0 = min(src, key=lambda m: m["when"] or datetime.datetime.max)
        for later in by_thread.get(m0["thread"], []):
            if later is m0 or later["sender"] != m0["sender"] or not later["when"] or not m0["when"]:
                continue
            days = (later["when"] - m0["when"]).total_seconds() / 86400
            if not 0 <= days <= WINDOW_DAYS:
                continue
            for r in RETRACT.finditer(later["own"]):
                key = (m0["file"], m0["sender"], later["when"], r.group(0).lower())
                if key in seen:
                    continue
                seen.add(key)
                hits += 1
                ctx = " ".join(later["own"][max(0, r.start() - 160):r.end() + 160].split())
                print(f"\n## {m0['name']} / {later['when']:%Y-%m-%d %H:%M} / {m0['subject'][:70]}")
                print(f"- quoted in: {where}")
                print(f"- quoted text: {q[:150]}")
                print(f"- later ({days:.1f} days): ...{ctx}...")
    print(f"\n# quotes resolved to a message: {resolved} / not resolved: {unresolved} / candidates: {hits}")
    print("# A candidate is for a person to read. No candidate is not proof of no retraction.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
