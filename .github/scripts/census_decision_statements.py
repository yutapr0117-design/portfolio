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
import datetime
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
# 候補の外で読む話題の語 (2026-11-12・portfolio-00 の依頼): 候補は「決める側が書いた会話」で選ぶので、撤回と放棄の
#   最も古い記録 (2000 年の "Wired Article on the GPL" 41 通など、理事が 1 人も書いていない会話) は語に関係なく外れる。
#   母数 (AS-OF の「候補 N 本」) は変えず、別の一覧として出す。irrevocable / non-revocability は revoc に含まれる
TOPIC = re.compile(r"revo[ck]|abandon", re.I)
TOPIC_MIN = 3   # 会話の本文 (引用を除く) で話題の語に当たる回数の下限


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


def _when(date):
    """Date 欄を比べられる時刻にする (タイムゾーンの無いものは UTC と読む)。読めなければ None。"""
    try:
        t = email.utils.parsedate_to_datetime(date)
    except (TypeError, ValueError, IndexError):
        return None
    return t if t.tzinfo else t.replace(tzinfo=datetime.timezone.utc)


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
        # 折り返した件名 (RFC 5322 の folding・次の行が空白で始まる) をつないで読む (2026-11-12): 1 行目だけを
        #   読むと "Draft of new OSI licenses landing page;⏎\tplease review." が "please review" を落とした別の鍵になり、
        #   rounds に置いた会話が「rounds に在るが READ-THREADS に無い」の照合から外れた (rounds の 100 file・408 件の件名)
        for m in re.finditer(r"^Subject:[ \t]*(.+(?:\n[ \t]+\S.*)*)", open(path, errors="replace").read(), re.M):
            k = title_key(" ".join(m.group(1).split()))
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


GAP_DAYS = 90


def _list_rows(path):
    """READ-THREADS.txt / THREAD-CANDIDATES.txt の行 [(件名の key, 日付, 件名)] (会話ごとに 1 行・同じ件名は複数行ありうる)。"""
    rows = []
    if path.exists():
        for line in open(path, encoding="utf-8"):
            if line.strip() and not line.startswith("#") and "\t" in line:
                date, title = line.rstrip("\n").split("\t", 1)
                if len(title_key(title)) >= 6:
                    rows.append((title_key(title), date, title))
    return rows


def conversations():
    """件名 key ごとに通を時刻順に並べ、通と通の間が GAP_DAYS を越えるところで会話に切る (2026-11-11・portfolio-00 と
    決めた)。件名だけでまとめると、年をまたいで同じ件名の別の会話が 1 本になり、1 つを読むと別の会話まで読了に数えて
    未読を少なく出していた (候補の件名 778 本のうち 48 本が複数の会話を含み、23 本は読了と記録されていた)。
    戻り値は {key: [(会話の最初の通の日付 ISO, 最後の通の時刻, [通…])]}。日付の読めない通は最初の会話に入れる。"""
    by_key = collections.defaultdict(list)
    for _, head, body in messages():
        title = subject_key(field(head, "Subject"))
        key = re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()[:90]
        if len(key) < 6:
            continue
        date = field(head, "Date")
        by_key[key].append((_when(date), date, field(head, "From"), title, body))
    convs = {}
    for key, v in by_key.items():
        groups, prev = [], None
        for x in sorted((x for x in v if x[0]), key=lambda x: x[0]):
            if prev is None or (x[0] - prev).days > GAP_DAYS:
                groups.append([])
            groups[-1].append(x)
            prev = x[0]
        undated = [x for x in v if not x[0]]
        if undated:
            (groups[0] if groups else groups.append([]) or groups[0]).extend(undated)
        convs[key] = [(_iso(g[0][1]), g[-1][0], g) for g in groups]
    return convs


def threads(out):
    listed = subprocess.check_output(["git", "-C", str(REPO), "ls-files", "LICENSES"], text=True).split()
    seen_in_dossier = set()
    for rel in listed:
        if rel.endswith(".md") and "/rounds/" not in rel:
            seen_in_dossier.update(grams(open(REPO / rel, errors="replace").read()))
    convs = conversations()
    rows, topical = [], []
    for key, cs in convs.items():
        for start, _end, g in cs:
            seen, n, words, hits, topic = set(), 0, 0, 0, 0
            for _t, date, sender, title, body in g:
                if (sender, date) in seen:
                    continue
                seen.add((sender, date))
                n += 1
                text = own_text(body)
                hits += sum(1 for gm in grams(text) if gm in seen_in_dossier)
                topic += len(TOPIC.findall(text))
                if DECIDERS.search(sender):
                    words += len(text.split())
            row = {"title": g[0][3], "first": g[0][1], "start": start, "key": key,
                   "messages": n, "decider_words": words, "dossier_hits": hits, "topic_hits": topic}
            if n >= 3 and words >= 120:
                rows.append(row)
            elif n >= 3 and topic >= TOPIC_MIN:
                topical.append(row)
    # 読了は READ-THREADS.txt だけから数える (portfolio-00 と 2026-11-09 に決めた)。行は会話を指す: 日付が会話の
    #   始まりと一致すればその会話、一致しなければ日付を含む会話 (無ければ日付より前で最も遅く始まる会話) に当て、
    #   一致しない行の数を出す (READ-THREADS の振り分けは portfolio-00)
    def to_conv(key, date):
        """一覧の行 (件名, 日付) が指す会話の始まり。一致しなければ日付を含む会話、無ければ日付より前で最も遅く始まる
        会話 (それも無ければ最初の会話)。アーカイブに件名が無ければ None。"""
        cs = convs.get(key, [])
        if not cs:
            return None
        hit = next((c for c in cs if c[0] == date), None) or next(
            (c for c in cs if c[0] <= date <= c[1].date().isoformat()), None) or max(
            (c for c in cs if c[0] <= date), key=lambda c: c[0], default=cs[0])
        return hit[0]

    read, off = set(), []
    for key, date, title in _list_rows(REPO / "LICENSES" / "READ-THREADS.txt"):
        start = to_conv(key, date)
        if start is not None and start != date:
            off.append(f"{date}\t{title} → {start}")
        read.add((key, start or date))
    in_rounds = rounds_titles()
    pinned_rows = _list_rows(CANDIDATES)
    # 固定も会話単位 (2026-11-11): 件名で固定すると、会話を 1 つ固定しただけで同じ件名の他の会話まで候補に入り、
    #   --pin のたびに一覧が増えて収束しなかった。件名単位で書かれた旧い行は、日付が指す会話に当てる
    pinned = {(k, to_conv(k, d) or d) for k, d, _t in pinned_rows}
    # 一度候補になった会話は外さない (THREAD-CANDIDATES.txt・2026-11-11): ドシエに語が入っただけで候補から外れ、
    #   読んでいないのに未読が減っていた
    candidates = [r for r in rows if r["dossier_hits"] < 8 or (r["key"], r["start"]) in read
                  or (r["key"], r["start"]) in pinned]
    pairs = {(r["key"], r["start"]) for r in candidates}
    # 一覧に在るのに閾値を満たさなくなった会話 (とアーカイブに件名の無い行) も母数に残す (portfolio-00 のレビュー)
    titles = {k: t for k, _d, t in pinned_rows}
    orphan = [{"title": titles[k], "first": d, "start": d, "key": k, "messages": 0, "decider_words": 0, "dossier_hits": 0}
              for k, d in sorted(pinned - pairs)]
    candidates += orphan
    is_read = lambda r: (r["key"], r["start"]) in read
    kept = [r for r in candidates if r["dossier_hits"] >= 8 and (r["key"], r["start"]) in pinned]
    new = [r for r in candidates if (r["key"], r["start"]) not in pinned]
    stale = [l for l in pinned_rows if (l[0], l[1]) not in pairs | pinned]
    if "--pin" in sys.argv and (new or stale):
        head = [l for l in open(CANDIDATES, encoding="utf-8") if l.startswith("#")] if CANDIDATES.exists() else []
        body = {f"{r['start']}\t{r['title']}\n" for r in candidates}
        CANDIDATES.write_text("".join(head) + "".join(sorted(body, key=lambda l: (l[:10], l))), encoding="utf-8")
    unread = sorted((r for r in candidates if not is_read(r)), key=lambda r: -r["decider_words"])
    json.dump(unread, open(out, "w"), ensure_ascii=False, indent=0)
    rounds_only = sorted((r for r in candidates if r["key"] in in_rounds and not is_read(r)), key=lambda r: -r["decider_words"])
    json.dump(rounds_only, open(str(out) + ".rounds-only.json", "w"), ensure_ascii=False, indent=0)
    print(f"conversations with deciders {len(rows)} (件名 + {GAP_DAYS} 日の空白で切った会話); few or no dossier hits "
          f"{len(candidates)}; of those, not read {len(unread)}")
    print(f"rounds に在るが READ-THREADS に無い（候補内 {len(rounds_only)} 件）: {out}.rounds-only.json")
    print(f"閾値から外れたが一覧に在る会話（{len(orphan)} 件・母数に残した）")
    # 候補の外で話題の語に当たる会話 (母数に入れない・AS-OF の数は動かない)
    topic_out = sorted((r for r in topical if (r["key"], r["start"]) not in pairs | pinned),
                       key=lambda r: (is_read(r), r["start"]))
    json.dump(topic_out, open(str(out) + ".topic-outside.json", "w"), ensure_ascii=False, indent=0)
    print(f"話題の語 ({TOPIC.pattern}・本文で {TOPIC_MIN} 回以上・3 通以上) に当たる候補の外の会話 {len(topic_out)} 件"
          f"（未読 {sum(1 for r in topic_out if not is_read(r))} 件・母数に入れない）: {out}.topic-outside.json")
    for r in (r for r in topic_out if not is_read(r)):
        print(f"  話題・未読: {r['start']}\t{r['title']}  (通 {r['messages']}・話題の語 {r['topic_hits']}・決める側の語 {r['decider_words']})")
    print(f"いまの語では候補でないが一覧に在る（{len(kept)} 件・うち未読 {sum(1 for r in kept if not is_read(r))} 件）")
    # そのうち未読の会話の名も出す (portfolio-00 の依頼・2026-11-11): ドシエが引用するほど語の当たりが増え、未読の
    #   会話が「候補の外・一覧に在る」へ移る。母数は一覧で固定されるので数は動かないが、どれが移ったかを AS-OF に
    #   書けるようにする (語の当たりの数は、候補の閾値 8 を越えた分だけ「読まずにドシエに語が入った」ことを示す)
    for r in sorted((r for r in kept if not is_read(r)), key=lambda r: r["start"]):
        print(f"  候補の外・未読: {r['start']}\t{r['title']}  (ドシエの語 {r['dossier_hits']}・決める側の語 {r['decider_words']})")
    print(f"READ-THREADS の行で、日付が会話の始まりと違う {len(off)} 行（日付を含む会話に当てた）" + ("" if not off else ""))
    for o in off:
        print(f"  {o}")
    print(f"一覧 (THREAD-CANDIDATES.txt) に無い候補の会話 {len(new)} 件・日付が会話の始まりでない一覧の行 {len(stale)} 行"
          + ("（--pin で一覧を作り直した）" if "--pin" in sys.argv and (new or stale) else "（--pin で一覧を作り直す）" if new or stale else ""))
    for r in sorted(new, key=lambda r: r["start"])[:20]:
        print(f"  新: {r['start']}\t{r['title']}  (通 {r['messages']}・決める側の語 {r['decider_words']}・ドシエの語 {r['dossier_hits']})")
    # ドシエが名を出しているのに未読の会話 (2026-11-12・portfolio-00 の依頼): 読んだのに READ-THREADS に足し忘れた
    #   会話 (0BSD-P は against #276 で読んだが行が無かった) を、件名 (3 語以上・Re: と [..] を除く) か件名の略称
    #   ("(0BSD-P)" の形) がドシエの本文 (rounds/ の外の LICENSES/*.md) に現れるかで拾う。一般的な件名
    #   ("License for approval" など) は別の文に一致しうるので、登録するかは人が読んで決める
    docs = {p.name: re.sub(r"\s+", " ", p.read_text(encoding="utf-8")) for p in sorted((REPO / "LICENSES").glob("*.md"))}
    cited = []
    for r in sorted((r for r in unread + topic_out if not is_read(r)), key=lambda r: r["start"]):
        core = re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", "", re.sub(r"^\s*(?:re|fwd?)\s*:\s*", "", r["title"], flags=re.I))).strip()
        acr = [a for a in re.findall(r"\(([A-Za-z0-9][A-Za-z0-9.\- ]{2,30})\)", r["title"])
               if re.search(r"[A-Z]", a) and re.search(r"[-0-9]", a)]
        pats = ([re.escape(core)] if len(core.split()) >= 3 else []) + [r"(?<![\w-])" + re.escape(a) + r"(?![\w-])" for a in acr]
        # 一致した文の前後 200 字に会話の始まりの年が在るか (portfolio-00 の依頼・2026-11-12): 一般的な件名は別の会話を
        #   指す文に一致しうるので、年が近くに在る file に「年」の印を添える (印が無くても別の会話とは限らない)
        where, near = [], set()
        for name, d in docs.items():
            ms = [m for p in pats for m in re.finditer(p, d, re.I)]
            if ms:
                where.append(name)
                if any(r["start"][:4] in d[max(0, m.start() - 200):m.end() + 200] for m in ms):
                    near.add(name)
        if where:
            cited.append((r, sorted(where), near))
    print(f"ドシエに件名か略称が現れる未読の会話 {len(cited)} 件 (読んだなら READ-THREADS に足す・一般的な件名は別の文の一致がある・"
          "「年」は一致の前後 200 字に会話の始まりの年が在る file)")
    for r, where, near in cited:
        names = [f"{n}{' [年]' if n in near else ''}" for n in where]
        print(f"  名が在る・未読: {r['start']}\t{r['title']}  ({', '.join(names[:4])}{' ほか' if len(names) > 4 else ''})")
    # AS-OF の「未読スレッドの残り」の行と同じ形 (Check 498 (h) が和を見る)
    print(f"AS-OF: 候補 {len(candidates)} 本のうち {len(candidates) - len(unread)} 本を読んだ。{len(unread)} 本は読んでいない")


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4) or sys.argv[1] not in ("rules", "threads", "noreview") or sys.argv[3:] not in ([], ["--pin"]):
        sys.exit(__doc__)
    {"rules": rules, "threads": threads, "noreview": noreview}[sys.argv[1]](sys.argv[2])
