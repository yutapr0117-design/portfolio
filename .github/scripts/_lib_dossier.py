"""_lib_dossier.py — ドシエの不利な事実の register (against) を読む場所を 1 か所にする。

against.md はバイトの予算 (Check 495) に近づいており、BLOCKING の手前で #N の番号を続けたまま 2 つ目の file へ分ける
(portfolio-00 と portfolio-9b の合意・2026-11-12)。その日に読み手を何か所も直さずに済むよう、file の一覧をここだけに置く。
分けた日は AGAINST_FILES に 2 つ目の file 名を足す (番号の範囲は file の順)。
"""
import re
from pathlib import Path

AGAINST_FILES = ("ACD-1.0.against.md",)


def against_paths(licenses_dir: Path) -> list[Path]:
    """register の file を順に (在るものだけ)。"""
    return [licenses_dir / n for n in AGAINST_FILES if (licenses_dir / n).exists()]


def against_text(licenses_dir: Path) -> str:
    """register の全 file の本文をつないだもの (無ければ空)。"""
    return "\n".join(p.read_text(encoding="utf-8") for p in against_paths(licenses_dir))


def is_against(name: str) -> bool:
    """file 名が register の file か。"""
    return name in AGAINST_FILES


# ── 草案の逐語の照合 (Check 468w / 468a が使う) ──────────────────────────────────────
def _parts(quote: str, minlen: int) -> list[str]:
    q = " ".join(quote.replace('\\"', '"').split())
    return [p for p in (" ".join(x.split()).strip(" ,;.:") for x in re.split(r"…|\.\.\.", q)) if len(p) > minlen]


def errata_draft_quote_misses(licenses_dir: Path, working_draft: Path) -> tuple[int, list[str]]:
    """468w: errata の各行が「N.M draft」として引く逐語が、その版の本文 (作業中ならその草案・凍結済みなら凍結した本文) に在るか。
    "draft" の後 200 字以内の最初の *"…"* を取り、"…" で切った 15 字を超える断片がすべて在ること。"as adopted"・行番号・
    "earlier version" の説明は除く (2026-11-11 に checks_license_draft.py で作り、2026-11-12 にここへ移した)。"""
    texts, n, miss = {}, 0, []
    for line in (licenses_dir / "ACD-1.0.errata.md").read_text(encoding="utf-8").split("\n"):
        me = re.match(r"^\|\s*\*{0,2}(E\d+)", line)
        if not me:
            continue
        for m in re.finditer(r"(?<![\d.])(\d+\.\d+) draft", line):
            v, tail = m.group(1), line[m.end():m.end() + 200]
            if re.match(r"\s*as adopted|\s*lines?\s+\d", tail) or "earlier version" in tail[:60] or '*"' not in tail:
                continue
            q = re.match(r'\*"(.+?)"\*', line[m.end() + tail.index('*"'):])
            if not q:
                continue
            if v not in texts:
                d, f = licenses_dir / f"ACD-{v}-DRAFT.txt", licenses_dir / f"ACD-{v}.txt"
                src = d if d == working_draft else f if f.exists() else None
                texts[v] = " ".join(src.read_text(encoding="utf-8").split()) if src else None
            n += 1
            lack = [x for x in _parts(q.group(1), 15) if texts[v] is None or x not in texts[v]]
            if lack:
                miss.append(f"{me.group(1)} ({v} draft): {lack[0][:60]!r}")
    return n, miss


_PAST_468A = re.compile(r"as adopted on|の前の形|T\d+ の前|旧い|旧文|\bwas\b|だった|外した|外れ|より前|earlier|formerly|used to|no longer")
_SKIP_468A = re.compile(r"CHANGELIST|TRIAL|SELF-AUDIT|ADVERSARIAL|RESEARCH-RECORDS|errata|BLIND-SPOTS|AUDIT-LEDGER|discussion-log")


def dossier_draft_quote_misses(licenses_dir: Path, version: str, draft_text: str) -> tuple[int, list[str]]:
    """468a: ドシエ (作業記録と errata を除く LICENSES/*.md) が「N.M draft / N.M 草案 / N.M の草案」の後 80 字以内に引く
    逐語が、いまの草案に在るか (2026-11-12・portfolio-00 の提案: 日付つきの注記が後の試作で古くなる)。前後に過去の形の印が
    あれば除き、草案の語と引用の間に「氏」があれば審査者の文として除く。"…" で切った 8 字を超える断片を当てる。"""
    flat_draft = " ".join(draft_text.split())
    n, miss = 0, []
    for f in sorted(licenses_dir.glob("*.md")):
        if _SKIP_468A.search(f.name):
            continue
        for i, line in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
            for m in re.finditer(re.escape(version) + r" (?:draft|草案|の草案)", line):
                tail = line[m.end():m.end() + 80]
                qm = re.search(r'\*"(.{12,}?)"\*', tail)
                if not qm or '*"' in tail[:qm.start()] or "氏" in tail[:qm.start()]:
                    continue
                n += 1
                if all(p in flat_draft for p in _parts(qm.group(1), 8)):
                    continue
                if not _PAST_468A.search(line[max(0, m.start() - 200):m.end() + 300]):
                    miss.append(f"{f.name}:{i} {qm.group(1)[:50]!r}")
    return n, miss


# ── 質問集の問数 (Check 460 (w) が使う・2026-11-15 に checks_license_self_reporting.py から移した) ──────────────
def counsel_question_count_misses(licenses_dir: Path, mirror_dir: Path) -> list[str]:
    """QUESTIONS-FOR-COUNSEL を名指す行の問数が、その file の見出し `## N.` の数と合わない箇所。

    11-01 に問 9 を足したのに REVIEWERS.md が「Eight questions」のまま残った。数の前の \\b を (?<![0-9]) に
    したのは「全8問」の 全 と 8 がどちらも語の文字で \\b が立たず数えなかったため (2026-11-12・監査 #135)。
    質問集とその mirror の中では、名前を書かない「尋ねたい N 問」「全 N 問」の行も読む。
    """
    qfc = licenses_dir / "QUESTIONS-FOR-COUNSEL.md"
    nq = len(re.findall(r"(?m)^## \d+\.", qfc.read_text(encoding="utf-8"))) if qfc.exists() else 0
    words = dict(zip("one two three four five six seven eight nine ten eleven twelve".split(), range(1, 13)))
    rx = re.compile(r"(?<!第)(?<!第 )(?<![0-9])(\d+) ?問|\b(" + "|".join(words) + r") questions\b|\ball ("
                    + "|".join(words) + r")\b", re.I)
    bad = []
    for p in sorted(licenses_dir.glob("*.md")) + sorted(mirror_dir.glob("*.md")):
        if is_against(p.name):
            continue
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            named = "QUESTIONS-FOR-COUNSEL" in line or (
                p.name.startswith("QUESTIONS-FOR-COUNSEL") and re.search(r"(?:全|尋ねたい|計) ?\d+ ?問", line))
            hits = list(rx.finditer(line)) if named else []
            g = hits[-1] if hits else None
            if g and (int(g.group(1)) if g.group(1) else words[(g.group(2) or g.group(3)).lower()]) != nq:
                bad.append(f"(w) {p.name}:{n} が質問集を {g.group(0)!r} と述べる / 実数 {nq}")
    return bad


# ── ドシエが自分の規模を述べる数の場所 (sync_stated_counts.py --apply が書き換える・2026-11-15・30 の依頼) ─────────
_ONES = ("one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen "
         "sixteen seventeen eighteen nineteen").split()
_TENS = "twenty thirty forty fifty sixty seventy eighty ninety".split()


def number_word(n: int, capital: bool = False) -> str:
    """1〜99 を英語の数詞に ("eighty-two")。capital なら頭を大文字に。"""
    w = _ONES[n - 1] if n < 20 else _TENS[n // 10 - 2] + ("" if n % 10 == 0 else "-" + _ONES[n % 10 - 1])
    return w[:1].upper() + w[1:] if capital else w


def _word_value(w: str) -> int | None:
    w = w.lower()
    for n in range(1, 100):
        if number_word(n) == w:
            return n
    return None


def dossier_counts(licenses_dir: Path) -> dict:
    """ドシエの規模の実測: 不利な事実の行・errata の行・worked entries の総数 (Check 460 (f) と同じ数え方)。"""
    ag = against_text(licenses_dir)
    er = (licenses_dir / "ACD-1.0.errata.md").read_text(encoding="utf-8")
    tot = 0
    for f in sorted(licenses_dir.glob("*.md")):
        ft = f.read_text(encoding="utf-8")
        tot += len(re.findall(r"^\*\*Q\.|^### (?:Q|A|B)\d+[a-z]?(?:-\d+)?\.", ft, re.M))
        if is_against(f.name):
            tot += len(re.findall(r"^\| \d+ \|", ft, re.M))
    closed = []
    for line in er.split("\n"):
        if re.match(r"^\|\s*\*{0,2}E\d+", line):
            c = re.split(r"(?<!\\)\|", line)
            if re.search(r"\d+\.\d+ 草案で閉じた", c[-2]):
                closed.append(c[1].strip().strip("*"))
    return {"against": len(re.findall(r"^\| \d+ \|", ag, re.M)),
            "errata": len(re.findall(r"^\| E\d+ \|", er, re.M)),
            "worked": tot, "closed": closed}


def count_sites(licenses_dir: Path) -> list[dict]:
    """ドシエが自分の規模を述べる数の場所 (_lib_draft_counts.length_sites と同じ形の dict)。

    不利な事実を 1 行足すたびに 6〜7 か所を手で直していた (30・2026-11-15 は 2 回)。照らすのは Check 460 (e)(f)(g) と
    §4c・errata 冒頭 (l)(v) で、ここはその申告を書き換える側である。照合の正規表現は Check 460 にあり、書き換えた後に
    verify を回せば食い違いは RED で出る。
    """
    c = dossier_counts(licenses_dir)
    rules = [  # (file 名, 正規表現, 各 group の値)
        ("ACD-1.0.against.md", r"grown\s+from\s+\d+\s+entries\s+to\s+\*\*(\d+)\*\*", [c["against"]]),
        ("ACD-1.0.against.md", r"produced\s+\*\*(\d+)\s+adverse\s+facts", [c["against"]]),
        ("ACD-1.0.against.md", r"(\d+)\s+errata\b", [c["errata"]]),
        ("REVIEWERS.md", r"(\d+) worked entries, indexed by the question", [c["worked"]]),
        ("REVIEWERS.md", r"All (\d+) adverse facts", [c["against"]]),
        ("REVIEWERS.md", r"(\d+) known imprecisions", [c["errata"]]),
        ("READY-TO-SUBMIT.md", r"\*\*(\d+) 件の不利な事実\*\*と \*\*(\d+) 件の errata\*\*", [c["against"], c["errata"]]),
        ("QUESTION-INDEX.md", r"There are \*\*(\d+)\*\* worked entries", [c["worked"]]),
        ("ACD-1.0.submission-reference.md", r"\*\*(\d+) entries, 1–(\d+), no gaps", [c["against"], c["against"]]),
    ]
    sites = []
    for name, rx, vals in rules:
        p = licenses_dir / name
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")  # file 全体で読む (Check 460 (e) と同じく、語の間の改行を \s+ が越える)
        for m in re.finditer(rx, text):
            for gi, v in enumerate(vals, 1):
                sites.append({"path": p, "line": text[:m.start(gi)].count("\n") + 1, "abs": True,
                              "start": m.start(gi), "end": m.end(gi), "old": m.group(gi), "new": str(v),
                              "what": f"{name} の {rx[:30]}"})
    # errata 冒頭: "**Eighty-two items are recorded, and all eighty-two are unrepaired …** — **eighty of them (E1, …) are closed"
    er = licenses_dir / "ACD-1.0.errata.md"
    lines = er.read_text(encoding="utf-8").split("\n")
    base = 0
    for ln, line in enumerate(lines, 1):
        off, base = base, base + len(line) + 1  # 行の頭の位置 (場所は file 全体の位置で持つ)
        m = re.search(r"\*\*([A-Z][a-z]+(?:-[a-z]+)?) items are recorded, and all ([a-z]+(?:-[a-z]+)?) are unrepaired", line)
        if m:
            for gi, cap in ((1, True), (2, False)):
                if _word_value(m.group(gi)):
                    sites.append({"path": er, "line": ln, "abs": True, "start": off + m.start(gi), "end": off + m.end(gi),
                                  "old": m.group(gi), "new": number_word(c["errata"], cap), "what": "errata 冒頭の件数の数詞"})
        m = re.search(r"\*\*([a-z]+(?:-[a-z]+)?) of them \(((?:E\d+, )*E\d+)\) are closed", line)
        if m and _word_value(m.group(1)):
            ids = sorted(c["closed"], key=lambda e: int(e[1:]))
            sites.append({"path": er, "line": ln, "abs": True, "start": off + m.start(1), "end": off + m.end(1),
                          "old": m.group(1), "new": number_word(len(ids)), "what": "errata 冒頭の閉じた件数の数詞"})
            sites.append({"path": er, "line": ln, "abs": True, "start": off + m.start(2), "end": off + m.end(2),
                          "old": m.group(2), "new": ", ".join(ids), "what": "errata 冒頭の閉じた番号の一覧"})
    return sites


# ── 審査者向けの文書が英語の入口から辿れること (Check 459c が使う・2026-11-15) ───────────────────────
_REVIEWER_AUDIENCE = re.compile(r"participants|licen[cs]e reviewers", re.I)


def reviewer_map_misses(licenses_dir: Path) -> tuple[int, list[str]]:
    """audience が審査者 (`… participants` / `licence reviewers`) の LICENSES/*.md が、REVIEWERS.md に名前を持つこと。

    名前を持たない文書は、frontmatter の `reachable-via: <file>` で、REVIEWERS.md に名前を持ち本文がこの文書を名指す
    親を宣言する (続きの冊・切り出した節)。50 の提案: Check 459 は LICENSES/README の索引への到達しか見ず、英語で
    審査者向けに書かれた QUESTIONS-FOR-PRACTITIONERS.md が入口 (REVIEWERS.md) から辿れなかった (#3149 で手で足した)。
    返り値: (照らした文書の数, 誤りの文の list)。
    """
    rv = licenses_dir / "REVIEWERS.md"
    rvt = rv.read_text(encoding="utf-8") if rv.exists() else ""
    n, bad = 0, []
    # 作業中の草案の版の文書 (ACD-<草案の版>-…) はまだ提出していないので対象外 (確定の日に新しい CHANGELIST が
    #   1 つ前の audience を写して RED になった・2026-11-15 の試走)
    drafts = [p for p in licenses_dir.glob("ACD-*-DRAFT.txt") if "HAS BEEN FROZEN" not in p.read_text(encoding="utf-8").split("\n", 1)[0]]
    wip = f"ACD-{drafts[0].name.split('-')[1]}-" if len(drafts) == 1 else None
    for p in sorted(licenses_dir.glob("*.md")):
        if p.name in ("REVIEWERS.md", "README.md") or (wip and p.name.startswith(wip)):
            continue
        head = p.read_text(encoding="utf-8").split("\n---", 1)[0]
        aud = re.search(r"^audience:(.*)$", head, re.M)
        if not aud or not _REVIEWER_AUDIENCE.search(aud.group(1)):
            continue
        n += 1
        if p.name in rvt:
            continue
        via = re.search(r"^reachable-via:\s*(\S+)", head, re.M)
        parent = licenses_dir / via.group(1) if via else None
        if not via:
            bad.append(f"459c: {p.name} は審査者向け (audience) なのに REVIEWERS.md に名前が無い。"
                       "地図の表に行を足すか、frontmatter に `reachable-via: <親の file>` を書く")
        elif not parent.exists() or parent.name not in rvt or p.name not in parent.read_text(encoding="utf-8"):
            bad.append(f"459c: {p.name} の reachable-via: {via.group(1)} が、REVIEWERS.md に名前を持ちこの文書を名指す親になっていない")
    return n, bad
