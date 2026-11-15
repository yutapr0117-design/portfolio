"""_lib_draft_counts.py — 次版の草案について「書かれた数」を「数え直した数」と照らす関数 (Check 468 / 460 (x) が使う)。

2026-11-15 に checks_license_draft.py (予算 900) と checks_license_self_reporting.py (予算 875) が advisory を越えた
(どちらも 9b が同じ日に足した面の分)。Check 468 は 1 つの `# ── 468.` 区間、Check 460 の面は 469 (a) が
`# (x)` と append の組で数えるので、区間や面を module 間で分けられない。照合の本体だけをここへ移し、Check の側には
呼び出しとラベルと誤りの append を残す (予算表の注記「分けるなら面を helper 関数へ移す」のとおり)。
各関数は誤りの文の list を返し、読めないものを黙って 0 にしない。
"""
import re
from pathlib import Path

RULE = "-" * 80


def bullet_components(hdr: str, prev: dict, cur: dict, changed: set, prev_body: str, cur_body: str, prev_ver: str):
    """468n (箇条ごと): 冒頭の変更一覧の語数申告を、箇条のまとまりごとに本文の差と照らす。

    上の合計の照合は 1 本の等式なので、§1.2 と §4.2 の申告を入れ替えても緑だった (2026-11-15 に実測)。
    箇条は「変更」ごとに語を数える (文を §8.1 から §8.3 へ移した変更は §8.3 の箇条に両側の差を載せる) ので、
    条ごとの 1 対 1 では照らさない。箇条が名指す変わった条を辺にして箇条をまとめ (union-find)、まとまりごとに
    「申告の和 = その条たちの本文の差の和」を見る。条でない本文 (前文・見出し) は「条の外」にまとめる。
    「the words Sections 8.1 and 8.4 use」は語の出所を引くだけなので辺にしない (含めると 19 箇条が 1 つに
    つながり、照合がほぼ合計と同じになる)。読むのは「Changes in this draft」の後の箇条だけ。
    返り値: (まとまり [(申告の和, 条の集合, 箇条の数)], 誤りの文の list)
    """
    bad, comps = [], []
    delta = {k: len(cur.get(k, "").split()) - len(prev.get(k, "").split()) for k in changed}
    outside = (len(cur_body.split()) - len(prev_body.split())) - sum(delta.values())
    parts = hdr.split("Changes in this draft", 1)
    if len(parts) < 2:
        bad.append("468n (箇条ごと): 冒頭に「Changes in this draft」が無く、変更の箇条を区切れない")
    for b in (" ".join(b.split()) for b in re.split(r"\n    \* ", parts[-1])[1:]):
        if "This draft:" in b:
            continue
        md = re.search(r"\((?:([+-])(\d+)|0) words?\.?\)", b)
        if not md:
            bad.append(f"468n (箇条ごと): 語数の申告 (+N / -N / 0 words.) が無い箇条: {b[:60]!r}")
            continue
        dec = int(md.group(1) + md.group(2)) if md.group(1) else 0
        named = re.sub(r"the words? (?:that )?Sections? (?:\d+\.\d+|[^,.()])*? uses?\b", "", b)
        s = {k for k in re.findall(r"\b(\d+\.\d+)\b", named) if k in changed} or {"<条の外>"}
        new = [dec, set(s), 1]
        for c in [c for c in comps if c[1] & s]:
            comps.remove(c)
            new = [new[0] + c[0], new[1] | c[1], new[2] + c[2]]
        comps.append(new)
    for dec, s, n in comps:
        act = sum(delta.get(k, 0) for k in s) + (outside if "<条の外>" in s else 0)
        if act != dec:
            bad.append(f"468n (箇条ごと): {n} 箇条のまとまり {sorted(s)} の申告 {dec:+d} が、それらの条の ACD-{prev_ver} "
                       f"からの本文の差 {act:+d} と一致しない (箇条間の取り違え・打ち消し合う 2 つの誤り)")
    return comps, bad


def changelist_table_total(path: Path):
    """468s: CHANGELIST の主表 (「## 表」〜「## errata 由来」) の「費用（語）」列 (右から 2 列目) の合計。

    返り値: (行の数, 合計, 読めない行の頭) か、区間が無ければ None。読めないセルは 0 扱いにしない。
    """
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    i, j = text.find("\n## 表"), text.find("\n## errata 由来")
    if i < 0 or j < i:
        return None
    rows = [ln for ln in text[i:j].split("\n") if ln.startswith("|") and not ln.startswith(("| 対象", "| :--"))]
    total, unread = 0, []
    for ln in rows:
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", ln.strip().strip("|"))]
        mc = re.match(r"([+\-−]?)\s*(\d+)", cells[-2]) if len(cells) >= 2 else None
        if not mc:
            unread.append(cells[0][:30])
            continue
        total += -int(mc.group(2)) if mc.group(1) in ("-", "−") else int(mc.group(2))
    return len(rows), total, unread


def draft_length_claims(lic: Path, skip) -> tuple[int, list[str]]:
    """460 (x): 外向きの文書が「いまの草案」の長さとして述べる数を、草案の実測と照らす。

    B3 の見出しと SUBMISSION-MATERIALS の長さの行は「N.M 草案は題名から 5,555 語で GPL-3.0 より 89 語短く、条文では
    597 語長い」と現在形で述べるが、Check 468 が照らすのは草案冒頭の申告だけで、この行は誰も見ていなかった
    (2026-11-15・1c の T61/T62 の +18 語で 8 箇所が黙って古くなるところだった)。読むのは「N.M 草案は」を含む行の、
    最初の日付つきの追記 (**2026- / （2026-) より前だけ (後ろは当時の記録)。英語の "N words from the title to
    *END OF TERMS*" は読まない —— 498 (j) が CHANGELIST では ADVISORY と決めている「1.0 から何が変わったか」の下書き。
    数え方: 題名から = 区切り線の後から END OF TERMS まで、条文 = `1.` の見出しから END OF TERMS の手前まで。
    GPL-3.0 の数は reviewer-positions.md の表から読み、読めなければ誤り (黙って定数にしない)。
    返り値: (照らした箇所の数, 誤りの文の list)。skip(file 名) が真の file は読まない。
    """
    drafts = [p for p in sorted(lic.glob("ACD-*-DRAFT.txt"))
              if "HAS BEEN FROZEN" not in p.read_text(encoding="utf-8").split("\n", 1)[0]]
    gpl = re.search(r"^\| GPL-3\.0 \| \*\*([\d,]+)\*\* \| \*\*([\d,]+)\*\* \|",
                    (lic / "ACD-1.0.reviewer-positions.md").read_text(encoding="utf-8"), re.M)
    if len(drafts) != 1 or not gpl:
        return 0, [f"(x) 作業中の草案がちょうど 1 つでない ({[p.name for p in drafts]}) か、"
                   "reviewer-positions.md の GPL-3.0 の行 (題名から / 条文) を読めない"]
    ver = re.match(r"ACD-(\d+\.\d+)-DRAFT", drafts[0].name).group(1)
    body = drafts[0].read_text(encoding="utf-8").split(RULE, 1)[-1]
    end, sec1 = body.find("END OF TERMS"), re.search(r"^1\.\s", body, re.M)
    title = len(body[:end + len("END OF TERMS")].split())
    ops = len(body[sec1.start():end].split()) if sec1 and end > 0 else -1
    g_title, g_ops = (int(g.replace(",", "")) for g in gpl.groups())
    want = [  # (正規表現, 正しい値, 何の数か)
        (r"題名から(?:は)? ?([\d,]+) ?語", title, "題名からの語数"),
        (r"GPL-3\.0[^。、]*?より ?([\d,]+) ?語短", g_title - title, "題名からの GPL-3.0 との差"),
        (r"END OF TERMS\*? ?(?:の手前)?までが ?([\d,]+) ?語", ops, "条文の語数"),
        (r"条文では ?([\d,]+) ?語長い", ops - g_ops, "条文の GPL-3.0 との差"),
        (r"同じ数え方で [\d,]+ ?語・\+([\d,]+)", ops - g_ops, "条文の GPL-3.0 との差"),
    ]
    n, bad = 0, []
    for p in sorted(lic.glob("*.md")) + sorted((lic.parent / "docs/files/LICENSES").glob("*.md")):
        if skip(p.name) or "CLARITY-TRIAL" in p.name:
            continue
        for ln, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if f"{ver} 草案は" not in line:
                continue
            seg = line[line.index(f"{ver} 草案は"):]
            cut = re.search(r"\*\*20\d\d-\d\d-\d\d|（20\d\d-\d\d-\d\d", seg)
            seg = seg[:cut.start()] if cut else seg
            for rx, v, what in want:
                for m in re.finditer(rx, seg):
                    n += 1
                    if int(m.group(1).replace(",", "")) != v:
                        bad.append(f"(x) {p.name}:{ln} の{what} {m.group(0)!r} / 草案の実測から {v}")
    if not n:
        bad.append("(x) 草案の長さを述べる行が 1 つも見つからない (B3 と SUBMISSION-MATERIALS の長さの行の形が"
                   "変わったなら本 face を直すこと —— 無いと黙る gate にしない)")
    return n, bad


def defined_term_uses(clauses: dict) -> tuple[dict, list[str]]:
    """468 (定義語): 定義した語が、定義した条の外で 1 回以上使われること。

    1c の試作は語を外す方向 (T54 の −105 語、T64 の apply) が続き、定義だけが残って使い先の無い語ができうる。
    使われない定義は「何のために在るか」を審査者に問わせ、残った定義が別の読みを生む。定義の形は §1 の
    `"X" means / includes / has the meaning / refers to` と、`In this Dedication, "X"` / `In Section N.M, "X"`。
    数え方は 1.0 の §4c と同じ (定義した条を除いた本文での出現・複数形の s を含む)。
    返り値: ({語: 使われた回数}, 誤りの文の list)。定義が 1 つも読めなければ誤り。
    """
    defs = []
    for k, v in clauses.items():
        for m in re.finditer(r'"([A-Z][A-Za-z\-]+(?: [A-Z][A-Za-z\-]+)*)"\s+(?:means|includes|has the meaning|refers to)', v):
            defs.append((m.group(1), k))
        for m in re.finditer(r'(?:In this Dedication|In Section \d+\.\d+), "([^"]+)"', v):
            defs.append((m.group(1), k))
    uses = {}
    for term, k in defs:
        rest = " ".join(v for kk, v in clauses.items() if kk != k)
        uses[term] = len(re.findall(r"\b" + re.escape(term) + r"s?\b", rest))
    bad = [f"468 (定義語): §{k} が定義する \"{t}\" が、定義の外で 1 回も使われていない" for t, k in defs if not uses[t]]
    if not defs:
        bad.append("468 (定義語): 草案から定義を 1 つも読めない (定義の形が変わったなら関数を直すこと)")
    return uses, bad
