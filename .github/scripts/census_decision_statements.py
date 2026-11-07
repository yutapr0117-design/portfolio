#!/usr/bin/env python3
"""決める側の発言から、規則の形の文と未読のスレッドを全期間で取り出す。

**CI には入れない** —— 手で走らせる道具で、入力は公開アーカイブの写しである。
キャッシュ先は `archive_census.py` と同じ形（`<list>-<YYYY>-<Month>.txt` を並べた
ディレクトリ）。

使い方:
    DOSSIER_ARCHIVE_CACHE=<dir> python3 .github/scripts/census_decision_statements.py rules <out.json>
    DOSSIER_ARCHIVE_CACHE=<dir> python3 .github/scripts/census_decision_statements.py threads <out.json>

`rules`: 下の DECIDERS の差出人の本文から、承認や適合について規則の形をした文を
抜き出す。`reviewer-positions.md` §1.140 はこの出力を読んだ記録である。

`threads`: 同じ差出人が発言したスレッドのうち、ドシエの分析文書に 8 語連鎖が
ほとんど現れないものを並べる。未読の候補であって、未読の証明ではない。

**どちらも下限である。** 正規表現なので言い回しが違う文は取りこぼす。差出人の名前は
議事録の出席者と主な審査者から手で選んだ。
"""
import collections
import email.utils
import glob
import json
import os
import pathlib
import re
import subprocess
import sys

CACHE = pathlib.Path(os.environ.get("DOSSIER_ARCHIVE_CACHE", "archive-cache"))
REPO = pathlib.Path(__file__).resolve().parents[2]
SPLIT = re.compile(r"^From \S+ at \S+  \w{3} \w{3} [ \d]\d \d\d:\d\d:\d\d \d{4}\s*$", re.M)
DECIDERS = re.compile("|".join(re.escape(x) for x in [
    "Tiemann", "Danese Cooper", "Coar", "Radcliffe", "Rishab", "Souza", "Nelson", "Nwakanma",
    "Alolita", "Tracy Hinds", "Maracke", "Piana", "Aniszczyk", "Choudhury", "Carrez", "Majerus",
    "Prabhakar", "Blondelle", "Berkus", "Greant", "Gune", "Garbee", "Suehle", "Michlmayr",
    "Oliver", "Asay", "Weerawarana", "Deb Bryant", "Colannino", "Maffulli", "Freund", "Raymond",
    "DiBona", "Mathur", "Chestek", "Fogel", "Mallet", "Chris Lamb", "Nicholson", "Phipps",
    "Hashman", "Liambotis", "Josh Simmons", "Vignoli", "Zacchiroli", "Villa", "Rosen", "Perens",
    "Fontana", "McCoy", "Behlendorf", "Vidal", "Kuhn", "Wheeler", "Dolan", "Sado", "Randal",
    "Milinkovich", "Langel",
]))
RULE = re.compile(r"""(
 \b(?:osi|we|the\ board|the\ committee|lrc|board|committee)\b[^.?!\n]{0,60}\b(?:will\ not|won't|wouldn't|would\ not|cannot|can't|should\ not|shouldn't|must\ not|never|refuse[sd]?|reject(?:s|ed)?|decline[sd]?|don't|do\ not|does\ not|doesn't|did\ not)\b[^.?!\n]{0,60}\b(?:approv\w+|certif\w+|accept\w*|list\w*)\b
 |\b(?:should|must|cannot|can't|could)\ (?:not\ )?be\ (?:approved|rejected|disapproved|certified)\b
 |\b(?:not|isn't|never)\ (?:an?\ )?(?:open[- ]source|osd[- ](?:compliant|conformant)|approvable|osi[- ]approvable)\b
 |\b(?:violat\w+|fail\w*|conflict\w*|incompatible|inconsistent|contrar\w+|breach\w*)\b[^.?!\n]{0,50}\bOSD\b
 |\bOSD\s*(?:\#|section\s*|clause\s*|§\s*)?\d+\b
 |\bnot\ (?:an?\ )?(?:acceptable|permissible|allowed)\b[^.?!\n]{0,40}\b(?:licen[sc]e|OSD|open\ source)\b
 |\b(?:reason|grounds?|basis)\ (?:to|for)\ (?:reject\w*|disapprov\w*|den\w+|refus\w*)\b
 |\b(?:licen[sc]e|document|text)\b[^.?!\n]{0,40}\b(?:must|has\ to|needs?\ to|should\ have|is\ required\ to|may\ not|cannot)\b[^.?!\n]{0,60}
)""", re.I | re.X)
CONDITION = re.compile(
    r"copyleft|reciproc|source code|AGPL|\bGPL\b|network|SaaS|field of use|discriminat|commercial"
    r"|royalt|fee\b|export|military|endorse|SSPL|data portab", re.I)


def messages():
    for path in sorted(glob.glob(str(CACHE / "license-*.txt"))):
        text = open(path, errors="replace").read()
        marks = [m.start() for m in SPLIT.finditer(text)] + [len(text)]
        for a, b in zip(marks, marks[1:]):
            head, _, body = text[a:b].partition("\n\n")
            yield os.path.basename(path), head, body


def field(head, name):
    m = re.search(rf"^{name}: (.*(?:\n[ \t].*)*)", head, re.M)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def own_text(body):
    kept = []
    for line in body.split("\n"):
        if line.startswith("-------------- next part"):
            break
        if not re.match(r"\s*(>|\|)", line) and not re.match(r".*wrote:\s*$", line):
            kept.append(line)
    return "\n".join(kept)


def subject_key(subject):
    s = re.sub(r"=\?[^?]+\?[qQbB]\?[^?]*\?=", " ", subject)
    s = re.sub(r"^((\[[^\]]*\]|Re:|RE:|Fwd:|FW:|Aw:|AW:)\s*)+", "", s)
    s = re.sub(r"\s*[\[(]?(was|Was|WAS)[: ].*$", "", s)
    s = re.sub(r"^((\[[^\]]*\]|Re:|RE:)\s*)+", "", s).strip()
    return s


def rules(out):
    found, seen, total = [], set(), 0
    for name, head, body in messages():
        total += 1
        sender = field(head, "From")
        if not DECIDERS.search(sender):
            continue
        try:
            when = email.utils.parsedate_to_datetime(field(head, "Date")).date().isoformat()
        except (TypeError, ValueError):
            when = "?"
        flat = re.sub(r"\s+", " ", own_text(body))
        for sentence in re.split(r"(?<=[.?!])\s+(?=[A-Z\"'(*])", flat):
            if 25 < len(sentence) < 420 and RULE.search(sentence):
                key = re.sub(r"\W+", "", sentence.lower())[:90]
                if key not in seen:
                    seen.add(key)
                    found.append({"date": when, "from": sender, "subject": subject_key(field(head, "Subject")),
                                  "file": name, "sentence": sentence,
                                  "about_conditions": bool(CONDITION.search(sentence))})
    json.dump(found, open(out, "w"), ensure_ascii=False, indent=0)
    conditions = sum(1 for f in found if f["about_conditions"])
    print(f"messages {total}; sentences {len(found)}; about conditions {conditions}; others {len(found) - conditions}")


def grams(text, n=8):
    words = re.sub(r"[^a-z0-9]+", " ", text.lower()).split()
    return (hash(" ".join(words[i:i + n])) for i in range(max(0, len(words) - n + 1)))


def threads(out):
    listed = subprocess.check_output(["git", "-C", str(REPO), "ls-files", "LICENSES"], text=True).split()
    seen_in_dossier = set()
    for rel in listed:
        if rel.endswith(".md") and "/rounds/" not in rel:
            seen_in_dossier.update(grams(open(REPO / rel, errors="replace").read()))
    table = collections.defaultdict(lambda: {"messages": 0, "decider_words": 0, "dossier_hits": 0, "seen": set(), "first": ""})
    for _, head, body in messages():
        title = subject_key(field(head, "Subject"))
        key = re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()[:90]
        if len(key) < 6:
            continue
        sender, date = field(head, "From"), field(head, "Date")
        entry = table[key]
        if (sender, date) in entry["seen"]:
            continue
        entry["seen"].add((sender, date))
        text = own_text(body)
        entry["title"] = entry.get("title") or title
        entry["first"] = entry["first"] or date
        entry["messages"] += 1
        entry["dossier_hits"] += sum(1 for g in grams(text) if g in seen_in_dossier)
        if DECIDERS.search(sender):
            entry["decider_words"] += len(text.split())
    rows = [{k: v for k, v in e.items() if k != "seen"} for e in table.values()
            if e["messages"] >= 3 and e["decider_words"] >= 120]
    unread = [r for r in rows if r["dossier_hits"] < 8]
    unread.sort(key=lambda r: -r["decider_words"])
    json.dump(unread, open(out, "w"), ensure_ascii=False, indent=0)
    print(f"threads with deciders {len(rows)}; few or no dossier hits {len(unread)}")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("rules", "threads"):
        sys.exit(__doc__)
    {"rules": rules, "threads": threads}[sys.argv[1]](sys.argv[2])
