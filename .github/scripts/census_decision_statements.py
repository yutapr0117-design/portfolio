#!/usr/bin/env python3
"""決める側の発言から、規則の形の文と未読のスレッドを全期間で取り出す。

**CI には入れない** —— 手で走らせる道具で、入力は公開アーカイブの写しである。
キャッシュ先は `archive_census.py` と同じ形（`<list>-<YYYY>-<Month>.txt` を並べた
ディレクトリ）。

使い方:
    DOSSIER_ARCHIVE_CACHE=<dir> python3 .github/scripts/census_decision_statements.py rules <out.json>
    DOSSIER_ARCHIVE_CACHE=<dir> python3 .github/scripts/census_decision_statements.py threads <out.json> [--pin]
    DOSSIER_ARCHIVE_CACHE=<dir> python3 .github/scripts/census_decision_statements.py noreview <out.json>

`rules`: 下の DECIDERS の差出人の本文から、承認や適合について規則の形をした文を
抜き出す。`reviewer-positions.md` §1.140 はこの出力を読んだ記録である。

`threads`: 同じ差出人が発言したスレッドのうち、ドシエの分析文書に 8 語連鎖が
ほとんど現れず、`LICENSES/rounds/` に逐語で置いた通の件名にも無いものを並べる。
未読の候補であって、未読の証明ではない。rounds の件名で除いた数も出すので、AS-OF の
「未読スレッドの残り」を手で数え直さずに済む。

`noreview`: `license-review` の提出 (件名が For Approval / Approval / Submission の
スレッドの最初の通) のうち、提出者が本文で法的レビューの不在を自分で述べたものを数える。
`review-rules.md` §1.141 の「少なくとも 23 件」を再現するための面。**語で探すので下限で
ある**: 不在を別の言い回しで書いた提出、後続の通でだけ述べた提出、件名に提出の語を
持たない提出は数えない。逆に「弁護士ではない」は起草のレビューの不在を言っていない
ことがあるので、出力は文ごとに人が読む。2026-11-08 の実測: 提出 200 件のうち 13 件。§1.141 の
23 件は手で読んだ数で、返信で不在を述べた提出 (Public Software) と、この語の幅の外の言い回しを
含む。**道具が再現するのは 13 件までで、23 件の再現には手読みが要る。**

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


MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]


def _chrono(path):
    """`<list>-<YYYY>-<Month>.txt` を時系列で並べる鍵。名前の辞書順では April が March より前に来て、
    返信を「最初の通」と取り違えた (2026-11-08 に noreview の 23 件との照合で発覚)。"""
    m = re.search(r"-(\d{4})-([A-Za-z]+)\.txt$", path)
    return (path.rsplit("-", 2)[0], int(m.group(1)), MONTHS.index(m.group(2))) if m and m.group(2) in MONTHS else (path, 0, 0)


def messages():
    for path in sorted(glob.glob(str(CACHE / "license-*.txt")), key=_chrono):
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


def title_key(subject):
    return re.sub(r"[^a-z0-9]+", " ", subject_key(subject).lower()).strip()[:90]


CANDIDATES = REPO / "LICENSES" / "THREAD-CANDIDATES.txt"


def _list_keys(path):
    """READ-THREADS.txt / THREAD-CANDIDATES.txt の形 (`<日付>\\t<件名>`・# で始まる行は見出し) の件名の key。"""
    keys = {}
    if path.exists():
        for line in open(path, encoding="utf-8"):
            if line.strip() and not line.startswith("#") and "\t" in line:
                date, title = line.rstrip("\n").split("\t", 1)
                k = title_key(title)
                if len(k) >= 6:
                    keys.setdefault(k, (date, title))
    return keys


def _iso(date):
    try:
        return email.utils.parsedate_to_datetime(date).date().isoformat()
    except (TypeError, ValueError, IndexError):
        return (date or "")[:10]


def listed_titles():
    """`LICENSES/READ-THREADS.txt` の件名 (候補の一覧から読んだもの・rounds を置かずに読んだものを含む・
    portfolio-00 が 2026-11-09 に置いた)。"""
    keys = set()
    listed = REPO / "LICENSES" / "READ-THREADS.txt"
    if listed.exists():
        for line in open(listed, encoding="utf-8"):
            if line.strip() and not line.startswith("#") and "\t" in line:
                k = title_key(line.rstrip("\n").split("\t", 1)[1])
                if len(k) >= 6:
                    keys.add(k)
    return keys


def rounds_titles():
    """rounds/ に逐語で置いた通の件名。1 通だけ置いた別スレッドの件名も入るので、読了には数えない (2026-11-09)。"""
    keys = set()
    for path in (REPO / "LICENSES" / "rounds").glob("*.txt"):
        for m in re.finditer(r"^Subject:\s*(.+)$", open(path, errors="replace").read(), re.M):
            k = title_key(m.group(1))
            if len(k) >= 6:
                keys.add(k)
    return keys


SUBMISSION = re.compile(r"for (?:legacy )?approval|\bapproval\b|submission|submitting", re.I)
NO_REVIEW = re.compile(r"""(
 \bno\ (?:formal\ |professional\ |external\ )?legal\ (?:reviews?|advice|counsel|analys[ie]s)\b
 |\b(?:has|have)(?:\ not|n't)\ (?:yet\ )?been\ (?:any\ |a\ )?(?:formal\ |external\ |professional\ )?legal\ (?:reviews?|analys[ie]s)\b
 |\b(?:has|have)(?:\ not|n't)\ (?:yet\ )?(?:had|undergone|received)\ (?:a\ |any\ )?(?:formal\ |external\ )?legal\ (?:reviews?|analys[ie]s)\b
 |\bnot\ (?:been\ |yet\ been\ )?(?:legally\ )?(?:reviewed|drafted|vetted|checked|written)\ by\ (?:a\ |an\ |any\ )?(?:lawyer|attorney|counsel|legal)
 |\bnot\ (?:been\ |yet\ been\ )?legally\ (?:reviewed|vetted)\b
 |\bwithout\ (?:any\ )?(?:legal|lawyer|attorney)\ (?:review|input|advice|help)\b
 |\bno\ lawyer\b|\bnot\ a\ lawyer\b|\bI\ am\ not\ an?\ (?:lawyer|attorney)\b|\bI'm\ not\ an?\ (?:lawyer|attorney)\b|\bIANAL\b
 |\bdrafted\ by\ (?:a\ )?lawyer\s*[:?]?\s*no\b|\blegal\ review\s*:\s*(?:none|no)\b
)""", re.I | re.X)


def noreview(out):
    first, found = {}, []
    for name, head, body in messages():
        if not name.startswith("license-review"):
            continue
        title = subject_key(field(head, "Subject"))
        key = re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()[:90]
        if not SUBMISSION.search(title) or key in first:
            continue
        first[key] = True
        flat = re.sub(r"\s+", " ", own_text(body))
        hits = [x for x in re.split(r"(?<=[.?!])\s+", flat) if NO_REVIEW.search(x)]
        if hits:
            found.append({"date": field(head, "Date"), "from": field(head, "From"), "subject": title,
                          "file": name, "sentences": [h[:300] for h in hits[:3]]})
    json.dump(found, open(out, "w"), ensure_ascii=False, indent=0)
    print(f"submissions (first messages) {len(first)}; stating no legal review in their own words {len(found)} (a floor)")


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
    # 読了は READ-THREADS.txt だけから数える (portfolio-00 と 2026-11-09 に決めた): rounds/ の件名を読了に
    #   数えると、別スレッドの通を 1 通だけ置いたときにそのスレッドまで読了になり、未読が過小になる
    listed, in_rounds = listed_titles(), rounds_titles()
    read = listed
    # 候補の一覧から読んだスレッド (READ-THREADS.txt) は候補に残す: 読むとドシエに語が足されて dossier_hits が
    #   8 を越え、候補から外れるので、残さないと母数が読むほど縮む (2026-11-09・771 → 726 を実測)。rounds/ だけに
    #   在るスレッドは候補の一覧から来たとは限らないので、母数には足さない
    pinned = _list_keys(CANDIDATES)
    # 一度候補になったスレッドは外さない (THREAD-CANDIDATES.txt・2026-11-11): 未読のまま、ドシエに語が
    #   入っただけで候補から外れ、読んでいないのに未読が減っていた (§1.171 の語で 2 本が外れた)
    candidates = [r for r in rows if r["dossier_hits"] < 8 or title_key(r["title"]) in listed
                  or title_key(r["title"]) in pinned]
    # 一覧に在るのに rows (決める側の語の閾値) から外れた件名も母数に残す (portfolio-00 のレビュー・2026-11-11):
    #   いまは名簿もアーカイブも動かないが、名簿に人を足すと語数が変わり、一覧の件名が rows から落ちうる
    in_rows = {title_key(r["title"]) for r in candidates}
    orphan = [{"title": t, "first": d, "messages": 0, "decider_words": 0, "dossier_hits": 0}
              for k, (d, t) in pinned.items() if k not in in_rows]
    candidates += orphan
    kept = [r for r in candidates if r["dossier_hits"] >= 8 and title_key(r["title"]) in pinned]
    new = [r for r in candidates if title_key(r["title"]) not in pinned]
    if "--pin" in sys.argv and new:
        lines = [l for l in open(CANDIDATES, encoding="utf-8")] if CANDIDATES.exists() else []
        head = [l for l in lines if l.startswith("#")]
        body = [l for l in lines if l.strip() and not l.startswith("#")]
        body += [f"{_iso(r['first'])}\t{r['title']}\n" for r in new]
        CANDIDATES.write_text("".join(head) + "".join(sorted(set(body), key=lambda l: (l[:10], l))), encoding="utf-8")
    unread = [r for r in candidates if title_key(r["title"]) not in read]
    unread.sort(key=lambda r: -r["decider_words"])
    json.dump(unread, open(out, "w"), ensure_ascii=False, indent=0)
    rounds_only = sorted((r for r in candidates if title_key(r["title"]) in in_rounds - listed),
                         key=lambda r: -r["decider_words"])
    json.dump(rounds_only, open(str(out) + ".rounds-only.json", "w"), ensure_ascii=False, indent=0)
    print(f"threads with deciders {len(rows)}; few or no dossier hits {len(candidates)}; "
          f"of those, not in READ-THREADS.txt {len(unread)}")
    print(f"rounds に在るが READ-THREADS に無い（候補内 {len(rounds_only)} 件）: {out}.rounds-only.json")
    print(f"決める側の語の閾値から外れたが一覧に在る（{len(orphan)} 件・母数に残した）")
    print(f"いまの語では候補でないが一覧に在る（{len(kept)} 件・うち未読 "
          f"{sum(1 for r in kept if title_key(r['title']) not in listed)} 件）")
    print(f"一覧 (THREAD-CANDIDATES.txt) に無い新しい候補 {len(new)} 件"
          + ("（--pin で一覧に足した）" if "--pin" in sys.argv and new else "（--pin で一覧に足す）" if new else ""))
    # AS-OF の「未読スレッドの残り」の行と同じ形 (Check 498 (h) が和を見る)
    print(f"AS-OF: 候補 {len(candidates)} 本のうち {len(candidates) - len(unread)} 本を読んだ。{len(unread)} 本は読んでいない")


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4) or sys.argv[1] not in ("rules", "threads", "noreview") or sys.argv[3:] not in ([], ["--pin"]):
        sys.exit(__doc__)
    {"rules": rules, "threads": threads, "noreview": noreview}[sys.argv[1]](sys.argv[2])
