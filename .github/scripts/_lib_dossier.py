"""_lib_dossier.py — ドシエの不利な事実の register (against) を読む場所を 1 か所にする。

against.md はバイトの予算 (Check 495) に近づいており、BLOCKING の手前で #N の番号を続けたまま 2 つ目の file へ分ける
(portfolio-00 と portfolio-9b の合意・2026-11-12)。その日に読み手を何か所も直さずに済むよう、file の一覧をここだけに置く。
分けた日は AGAINST_FILES に 2 つ目の file 名を足す (番号の範囲は file の順)。

**分ける日の予行 (2026-11-15・9b)**: 使い捨ての worktree で後ろの表 (469〜609 行・393 KB) を `ACD-1.0.against-2.md` へ
移し、AGAINST_FILES に足して consistency を回すと 7 件が RED だった。読み手の欠陥 2 件 (472e の除外が固定名の startswith・
460 (g) の倍率の分子が 1 つ目の file だけ) と find_quote_retractions の固定名は、この予行の PR で against の一覧へ
寄せた。残るのは分ける日の作業で、どれも RED が知らせる: (1) README の索引に行 (459)、(2) frontmatter に last-updated
(461c) と `reachable-via: ACD-1.0.against.md` (459c)、(3) docs/files の mirror (108)、(4) BYTE-BUDGET-DATA に行 (495c)、
(5) 動かした行に anchor を持つ mutation の "file" を 2 つ目へ付け替える (362・予行では #162 の 2 件)。474 / 491 / 460 (e)
は against_text を読むので、行を動かしても黙らない (予行で確かめた)。
"""
import re
from pathlib import Path

AGAINST_FILES = ("ACD-1.0.against.md", "ACD-1.0.against-2.md")


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
    あれば除き、草案の語と引用の間に「氏」があれば審査者の文として除く。"…" で切った 8 字を超える断片を当てる。

    2026-11-24 (fc・mutation の全数の当て直しで MISSED): 作業中の版の「N.M 草案」しか読んでいなかったので、1.4 を確定した日から
    「1.4 草案」と書いた引用を 1 つも照らさなくなった (FAQ の *"a payment You agreed to make"* を別の語にしても黙っていた)。
    468w と同じく、作業中の版は草案に、凍結した版は凍結した本文 (区切り線より下) に当てる。"""
    texts = {version: " ".join(draft_text.split())}

    def body(v: str):
        if v not in texts:
            f = licenses_dir / f"ACD-{v}.txt"
            raw = f.read_text(encoding="utf-8") if f.exists() else None
            texts[v] = " ".join(raw.split("-" * 80, 1)[-1].split()) if raw else None
        return texts[v]
    n, miss = 0, []
    for f in sorted(licenses_dir.glob("*.md")):
        if _SKIP_468A.search(f.name):
            continue
        for i, line in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
            for m in re.finditer(r"(?<![\d.])(1\.[1-9]) (?:draft|草案|の草案)", line):
                flat_draft = body(m.group(1))
                if flat_draft is None:
                    continue
                tail = line[m.end():m.end() + 80]
                qm = re.search(r'\*"(.{12,}?)"\*', tail)
                if not qm or '*"' in tail[:qm.start()] or "氏" in tail[:qm.start()]:
                    continue
                n += 1
                if all(p in flat_draft for p in _parts(qm.group(1), 8)):
                    continue
                if not _PAST_468A.search(line[max(0, m.start() - 200):m.end() + 300]):
                    miss.append(f"{f.name}:{i} ({m.group(1)}) {qm.group(1)[:50]!r}")
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


def reviewer_map_misses(licenses_dir: Path, include_wip: bool = False) -> tuple[int, list[str]]:
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
    wip = f"ACD-{drafts[0].name.split('-')[1]}-" if len(drafts) == 1 and not include_wip else None
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


# ── ドシエの §1.N 見出しの重複 (Check 500 が使う・2026-11-15) ───────────────────────
SECTION_SERIES_FLOOR = 70  # これより小さい §1.N は文書ごとの番号 (comparison §1.3 と CHANGELIST §1.3 など・通し番号ではない)


def section_heading_duplicates(licenses_dir: Path) -> tuple[int, list[str]]:
    """LICENSES/*.md の `## 1.N` 見出し (N >= SECTION_SERIES_FLOOR) が、ドシエ全体で 1 か所にしか無いこと。

    §1.70 以降はドシエ全体の通し番号として、文書の名を添えずに引かれる (「§1.241」)。2026-11-15、未読の 285 本を
    5 人で読むため節番号を帯で分けた (2f §1.242〜・30 §1.300〜・50 §1.350〜・1c §1.400〜・9b §1.450〜)。帯を越えて
    同じ番号を 2 人が使うと、名を添えない引用がどちらの節かを決められなくなる。それより前の重複 (§1.67〜§1.69 が
    review-corpus と review-venue の両方に在る) は通し番号になる前の分割の名残で、床の下に在る。
    返り値: (照らした見出しの数, 重複の文の list)。
    """
    seen: dict[int, list[str]] = {}
    for p in sorted(licenses_dir.glob("*.md")):
        for m in re.finditer(r"^## 1\.(\d+)\b", p.read_text(encoding="utf-8"), re.M):
            if int(m.group(1)) >= SECTION_SERIES_FLOOR:
                seen.setdefault(int(m.group(1)), []).append(p.name)
    bad = [f"§1.{n}: {', '.join(v)}" for n, v in sorted(seen.items()) if len(v) > 1]
    return sum(len(v) for v in seen.values()), bad


# ── 読んだ節の「反映」の欄 (Check 501 が使う・2026-11-15) ───────────────────────
REFLECT_FROM = 242  # 5 人で未読を読む日 (2026-11-15) から書く節。それより前の節には欄が無い
_REFLECT_LINE = re.compile(r"^\*\*反映\*\*[:：][ \t]*(.*)$", re.M)
_REFLECT_VOCAB = re.compile(r"\bB\d+|against #\d+|errata E\d+|\b1c\b|THIRD|入口|なし（[^）]+）|未定")


def reflect_field_misses(licenses_dir: Path) -> tuple[int, list[str], list[str]]:
    """§1.242 以降の各節 (`## 1.N`) が「**反映**: …」の行を 1 つ持ち、行き先を語彙で述べること。

    オーナーの前提「未読があり、未反映のまま本申請は出せない」(2026-11-15) を受けた 2f の提案 (A)。読んだ節が
    どこへ効いたか (B の節・against の行・errata・1c への種・入口) を節ごとに書かせ、合成 (提案 (C)) の集計の鍵にする。
    語彙: B# / against #N / errata E# / 1c / THIRD / 入口 / なし（理由） / 未定。against #N と errata E# は実在を照らす
    (反映したと書いて行が無い形を止める)。返り値: (照らした節の数, RED の文, 未定の節 (ADVISORY))。
    """
    ag = against_text(licenses_dir)
    ag_rows = {int(n) for n in re.findall(r"^\| (\d+) \|", ag, re.M)}
    er = licenses_dir / "ACD-1.0.errata.md"
    er_rows = set(re.findall(r"^\| (E\d+) \|", er.read_text(encoding="utf-8"), re.M)) if er.exists() else set()
    n, bad, pending = 0, [], []
    for p in sorted(licenses_dir.glob("*.md")):
        t = p.read_text(encoding="utf-8")
        heads = list(re.finditer(r"^## 1\.(\d+)\b", t, re.M))
        for i, h in enumerate(heads):
            num = int(h.group(1))
            if num < REFLECT_FROM:
                continue
            n += 1
            nxt = re.search(r"^## ", t[h.end():], re.M)
            body = t[h.end(): h.end() + nxt.start()] if nxt else t[h.end():]
            lines = _REFLECT_LINE.findall(body)
            where = f"{p.name} §1.{num}"
            if len(lines) != 1 or not lines[0].strip():
                bad.append(f"{where}: 「**反映**: …」の行が {len(lines)} 行" + (" (空)" if lines and not lines[0].strip() else ""))
                continue
            v = lines[0]
            if not _REFLECT_VOCAB.search(v):
                bad.append(f"{where}: 反映の欄が語彙 (B# / against #N / errata E# / 1c / THIRD / 入口 / なし（理由） / 未定) で始まらない: {v[:60]}")
            for a in re.findall(r"against #(\d+)", v):
                if int(a) not in ag_rows:
                    bad.append(f"{where}: 反映の欄の against #{a} が register に無い")
            for e in re.findall(r"errata (E\d+)", v):
                if e not in er_rows:
                    bad.append(f"{where}: 反映の欄の errata {e} が errata に無い")
            if "未定" in v:
                pending.append(where)
    return n, bad, pending


# ── 古い節の反映の表 (REFLECTION-BACKFILL.md・Check 501 の 2 つ目の面・2026-11-15) ─────────────────
REFLECT_SCOPE_EXCLUDE = ("ACD-1.0.comparison.md", "REVISION-PROTOCOL.md")  # §1.N が読みの節でない文書 (CHANGELIST も外す)
# 表の行のうち反映が「未定」のもの (呼ぶたびに作り直す・2026-11-16): 節の末尾の欄の未定は reflect_field_misses が返すが、
#   表の行の未定はどこも数えておらず、gate_6c は 1.161 の未定の行を残したまま「満たした」と返した
BACKFILL_PENDING: list[str] = []
_BF_CELL = re.compile(r"^(?:`?(?P<file>[A-Za-z0-9.\-]+\.md)`?\s+|(?P<stem>[a-z][a-z0-9\-]+)\s+)?(?P<num>1\.\d+)$")


def _reflect_targets(licenses_dir: Path, cell: str, ag_lines: dict[int, str], er_lines: dict[str, str]) -> list[str]:
    """反映のセルが名指す行き先の本文 (against の行・errata の行・B の文書・名指した file)。"""
    out = [ag_lines.get(int(n), "") for n in re.findall(r"#(\d+)", cell)]
    out += [er_lines.get(e, "") for e in re.findall(r"\b(E\d+)\b", cell)]
    if re.search(r"\bB\d+\b", cell):
        out += [p.read_text(encoding="utf-8") for p in sorted(licenses_dir.glob("ACD-OSI-BOTTLENECKS*.md"))]
    for f in set(re.findall(r"`([A-Za-z0-9.\-]+\.md)`", cell)):
        p = licenses_dir / f
        if p.exists():
            out.append(p.read_text(encoding="utf-8"))
    return out


def backfill_table_misses(licenses_dir: Path) -> tuple[int, list[str], list[str]]:
    """REFLECTION-BACKFILL.md の表 (50 の依頼・2026-11-15): 行の番号が実在の `## 1.N` 見出しと 1 対 1 (重複なし・
    REFLECT_FROM 以降なし)。番号のセルは「1.179」か、床 (70) の下で文書ごとの番号のときは「`<file>` 1.67」(50 の形)。
    反映のセルは Check 501 の語彙で、against #N / errata E# は実在。「確かめ方」が grep と言う行は、名指した行き先の
    どれかに「§1.N」が実在すること (反映したと書いて行き先が引いていない形を止める)。
    返り値: (表の行の数, RED の文, 反映の無い節 (欄も行も無い・2026-11-16 から BLOCKING))。
    """
    ag = against_text(licenses_dir)
    ag_lines = {int(m.group(1)): m.group(0) for m in re.finditer(r"^\| (\d+) \|.*$", ag, re.M)}
    erp = licenses_dir / "ACD-1.0.errata.md"
    er_lines = {m.group(1): m.group(0) for m in re.finditer(r"^\| (E\d+) \|.*$", erp.read_text(encoding="utf-8"), re.M)} if erp.exists() else {}
    heads: dict[tuple[str, int], bool] = {}  # (file, N) -> 節の末尾に反映の欄が在るか
    for p in sorted(licenses_dir.glob("*.md")):
        if p.name in REFLECT_SCOPE_EXCLUDE or p.name.endswith("-CHANGELIST.md") or p.name == "REFLECTION-BACKFILL.md":
            continue
        t = p.read_text(encoding="utf-8")
        hs = list(re.finditer(r"^## 1\.(\d+)\b", t, re.M))
        for i, h in enumerate(hs):
            body = t[h.end(): hs[i + 1].start() if i + 1 < len(hs) else len(t)]
            heads[(p.name, int(h.group(1)))] = bool(_REFLECT_LINE.search(body))
    BACKFILL_PENDING.clear()
    bf = licenses_dir / "REFLECTION-BACKFILL.md"
    rows = [r for r in re.findall(r"^\|(.+)\|\s*$", bf.read_text(encoding="utf-8"), re.M)] if bf.exists() else []
    bad, covered = [], set()
    n = 0
    for r in rows:
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", r)]
        m = _BF_CELL.match(cells[0]) if cells else None
        if not m:
            # 飛ばすのは見出しの行 (節 | 反映 | 確かめ方) と区切りの行 (:--) だけ。それ以外を黙って飛ばすと、書いた人は表に足した
            #   つもりで照合だけ外れる (2026-11-15・50 の #3251 の「review-precedents 1.45」42 行・安全網の規律 (3))
            if cells and (cells[0] == "節" or re.fullmatch(r":?-{2,}:?", cells[0])):
                continue
            bad.append(f"REFLECTION-BACKFILL の行 {cells[0][:40]!r}: 番号のセルが「1.N」「`<file>.md` 1.N」「<名> 1.N」の形でない (照合から外れる)")
            continue
        n += 1
        num = int(m.group("num").split(".")[1])
        where = f"REFLECTION-BACKFILL の行 {cells[0]}"
        # 短い形「review-precedents 1.45」は ACD-1.0.<名>.md を指す (2026-11-15・5 人の表に 42 行がこの形で入った)。名が実在しなければ RED
        fname = m.group("file") or (f"ACD-1.0.{m.group('stem')}.md" if m.group("stem") else None)
        if fname and not (licenses_dir / fname).exists():
            bad.append(f"{where}: 文書 {fname} が無い")
            continue
        hits = [k for k in heads if k[1] == num and (not fname or k[0] == fname)]
        if len(hits) != 1:
            bad.append(f"{where}: 見出し `## 1.{num}` が {len(hits)} 個に当たる" + ("" if hits else " (無い)") +
                       ("" if m.group("file") or len(hits) < 2 else " —— 床の下の番号は「`<file>` 1.N」と書く"))
            continue
        k = hits[0]
        if num >= REFLECT_FROM:
            bad.append(f"{where}: §1.{REFLECT_FROM} 以降の節は節の末尾に欄を書く (表に置かない)")
        if k in covered:
            bad.append(f"{where}: 同じ節の行が 2 つ在る")
        if heads[k]:
            bad.append(f"{where}: 節の末尾にも反映の欄が在る (両方は置かない)")
        covered.add(k)
        v = cells[1] if len(cells) > 1 else ""
        if "未定" in v:
            BACKFILL_PENDING.append(where)
        if not _REFLECT_VOCAB.search(v):
            bad.append(f"{where}: 反映のセルが語彙で始まらない: {v[:50]}")
        for a in re.findall(r"against #(\d+)", v) + re.findall(r"(?<=[・、/ ])#(\d+)", v):
            if int(a) not in ag_lines:
                bad.append(f"{where}: 反映のセルの #{a} が register に無い")
        for e in re.findall(r"errata (E\d+)|\b(E\d+)\b", v):
            e = e[0] or e[1]
            if e not in er_lines:
                bad.append(f"{where}: 反映のセルの {e} が errata に無い")
        how = cells[2] if len(cells) > 2 else ""
        if "grep" in how and not v.startswith(("なし", "未定")):
            rx = re.compile(rf"§1\.{num}(?!\d)")
            # 床 (70) の下の番号は文書ごとの番号で、行き先の「§1.49」が別の文書の §1.49 のことがある (30 の指摘・50 経由・2026-11-15)。
            #   その範囲は、同じ行が文書の名 (`reviewer-positions` など) も持つときだけ当たりとする
            stem = k[0].removeprefix("ACD-1.0.").removesuffix(".md")
            ok = any(rx.search(ln) and (num >= SECTION_SERIES_FLOOR or stem in ln)
                     for x in _reflect_targets(licenses_dir, v, ag_lines, er_lines) for ln in x.split("\n"))
            if not ok:
                bad.append(f"{where}: 確かめ方は grep と言うが、名指した行き先のどれにも「§1.{num}」が無い"
                           + ("" if num >= SECTION_SERIES_FLOOR else f" (床の下の番号は同じ行に「{stem}」も要る)"))
    missing = [f"{f} §1.{num}" for (f, num), has in sorted(heads.items(), key=lambda x: (x[0][1], x[0][0]))
               if num < REFLECT_FROM and not has and (f, num) not in covered]
    return n, bad, missing


# ── 提出対象の版 (2026-11-23・議題 3 の下ごしらえ・fc) ───────────────────────────
def submission_target_version(licenses_dir: Path) -> str:
    """submission.md の `<!-- SUBMISSION-TARGET: ACD-x.y -->` の版 ("1.0" など)。読めなければ "1.0"。

    §4c の機械監査の表 (定義語・節・非 ASCII・記述子の条の参照・逐条の行) を照らす 460 (i)・(n) と 498 (d) は、ACD-1.0.txt と
    ACD-1.0.machine.json を名で読んでいた。提出対象を 1.4 へ切り替えると、表を 1.4 で測り直しても照合だけが 1.0 を見続ける。
    """
    sm = licenses_dir / "ACD-1.0.submission.md"
    m = re.search(r"<!--\s*SUBMISSION-TARGET:\s*ACD-(\d+\.\d+)\s*-->", sm.read_text(encoding="utf-8")) if sm.exists() else None
    return m.group(1) if m else "1.0"


# ── register の英語の索引の "Other side:" の欄 (Check 503・2026-11-23 の議題 7・5/0/0) ─────────────
_OTHER_BANNED = re.compile(r"^(?:none|n/?a|—|-|tbd|see (?:the )?japanese.*)$", re.I)


def register_other_side_misses(licenses_dir: Path) -> tuple[list[str], list[str]]:
    """日本語の行が **逆側** を持つ B について、英語の索引の行が "Other side: …" の句を持つこと。返り値: (対象の B, 誤りの文)。

    条件 (5 人の合議で決めた): 句は 5 語以上で、決まり文句 (none・n/a・—・TBD・see Japanese) でない / 対象の句どうしが同じ文でない /
    日本語の行の逆側の段に固有名 (英字の大文字で始まる語) か年 (YYYY) があれば、そのどれか 1 つが英語の句にも在る。句の向き
    (その行の結論と反対の側) は中身の規則で、機械は判定しない。英語の行は日本語の行の要約で、日本語の行に逆側を足しても
    英語の行は片側のまま黙ってずれた (B1・cd の報告)。語の印 (against・however …) で照らす形は 15 本中 8 本が誤検出だった。
    """
    t = (licenses_dir / "ACD-OSI-BOTTLENECKS.md").read_text(encoding="utf-8")
    en = {m.group(1): m.group(0) for m in re.finditer(r"^\| (B\d+) \|.*$", t, re.M)}
    ja = {m.group(1): m.group(0) for m in re.finditer(r"^\| \*\*(B\d+)\*\* \|.*$", t, re.M)}
    targets = sorted((b for b, row in ja.items() if "逆側" in row), key=lambda b: int(b[1:]))
    bad, seen = [], {}
    for b in targets:
        m = re.search(r"Other side:\s*([^|]*)", en.get(b, ""))
        phrase = " ".join(m.group(1).split()).strip(" .") if m else ""
        if not m:
            bad.append(f"{b}: 英語の行に \"Other side:\" の句が無い")
            continue
        if len(phrase.split()) < 5 or _OTHER_BANNED.match(phrase):
            bad.append(f"{b}: \"Other side:\" の句が 5 語未満か決まり文句 ({phrase[:40]!r})")
            continue
        if phrase in seen:
            bad.append(f"{b}: \"Other side:\" の句が {seen[phrase]} と同じ文")
        seen[phrase] = b
        side = ja[b][ja[b].index("逆側"):]
        anchors = set(re.findall(r"\b[A-Z][A-Za-z]{2,}\b|\b(?:19|20)\d\d\b", side)) - {"ACD", "OSI", "OSD", "The", "This", "Section"}
        if anchors and not any(re.search(r"\b" + re.escape(a) + r"\b", phrase) for a in anchors):
            bad.append(f"{b}: \"Other side:\" の句が、日本語の逆側の固有名か年 ({sorted(anchors)[:4]}) のどれも持たない")
    return targets, bad


# License Committee の委員長の在任 (YYYY-MM・両端を含む)。根拠 (2026-11-25 に引き直した):
#   Fontana     — 2019-01-10 の license-review に "the License Committee Chair (currently me)"。始まりは確かめていない。
#   Chestek     — 自分の署名 "Chair, License (Review) Committee" が 2019-05-24〜2025-02-14 に 191 通 (license-review / -discuss の写し)。
#                 議事録 2025-01-17 "appoint a new License committee chair as Pam's term on the board ends on April 1st"。
#   Berkus      — 議事録 2026-02-20 "his leadership as Chair of the License Committee" (過去形で労う)。**始まり (2025-03/04) は直接の
#                 記録が無い推定** (理事会ページの月次の写しと、Chestek 氏の任期の終わりから)。
#   McCoy Smith — 議事録 2026-03-20 "McCoy reports for the Licensing Committee"、2026-02-20 も同氏が状況を報告。
# 境目 (2019-02〜05・2025-03・2026-01〜02) は記録が月を決めないので、両方の人を許して止めない。委員長が替わった日に、根拠と一緒に直す
CHAIR_TERMS = {"Fontana": ("0000-00", "2019-05"), "Chestek": ("2019-02", "2025-03"), "Berkus": ("2025-03", "2026-02"),
               "McCoy Smith": ("2026-01", "9999-99")}


def chair_term_misses(files: list[Path]) -> tuple[int, list[str]]:
    """発言の月に委員長でなかった人を「委員長」「chair」と、委員長だった人を「のちの委員長」「元委員長」と書いた文。返り値: (拾った数, 誤り)。

    2026-11-25 (#4148 と同じ型の再発)。役・名・発言日が隣り合う 3 つの形だけを見る。役の直後に別の人の名が続く形 (日付の括弧の中の
    「委員長 Chestek 氏の…」)、役を否定する形 (委員長ではない)、「」で囲んだ言及は外す。日付が名から離れた文と、名の無い「委員長は」は
    見えない。「元・のちの」は境目の月を除いた在任のまっただ中だけを誤りにする。
    """
    name = "|".join(CHAIR_TERMS)
    role = r"(?:委員長(?!では|でな|職)|[Cc]hair\b)"
    day = r"(?P<d>(?:19|20)\d\d-\d\d)(?:-\d\d)?"
    forms = [
        re.compile(rf"{role}(?:の|・|（|\(|は|、|, | |「|Pamela|Josh)*\**(?P<n>{name})[^|。]{{0,12}}?{day}"),
        re.compile(rf"(?P<n>{name})(?: 氏)?[（(、・ ]*(?:のちの|後の|当時の|元)?{role}[^|。]{{0,12}}?{day}"),
        re.compile(rf"(?P<n>{name})\**(?: 氏)?(?: の)?[ 、]*{day}[（(][^）)]{{0,12}}?{role}(?! ?(?:の )?(?:Pamela |Josh )?(?:{name}))"),
    ]
    border = {"2019-02", "2019-03", "2019-04", "2019-05", "2025-03", "2026-01", "2026-02"}
    n, bad = 0, []
    for f in files:
        for i, ln in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
            for m in (m for p in forms for m in p.finditer(ln)):
                if ln[:m.start()].endswith("「") and "」" in ln[m.end():m.end() + 12]:
                    continue
                n += 1
                lo, hi = CHAIR_TERMS[m["n"]]
                inside = lo <= m["d"] <= hi
                other = re.search(r"元 ?委員長|のちの|後の ?委員長|former", ln[max(0, m.start() - 8):m.end()])
                if (other and inside and m["d"] not in border) or (not other and not inside):
                    bad.append(f"{f.name}:{i} 「{m.group(0)[:50]}」")
    return n, bad
