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
        # 「Sections 5.1 to 5.3」は端の 2 つだけでなく間の条も名指す (2026-11-19・冒頭の一覧を詰めると範囲の形が増える)
        named = re.sub(r"\b(\d+)\.(\d+) (?:to|through)(?: Sections?)? \1\.(\d+)\b",
                       lambda m: ", ".join(f"{m.group(1)}.{i}" for i in range(int(m.group(2)), int(m.group(3)) + 1)), named)
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


def _fmt(old: str, value: int) -> str:
    """old の書き方 (3 桁区切り・符号・全角のマイナス) を保って value を書く。"""
    sign = ""
    if old[:1] in "+-−":
        sign = old[0] if value < 0 and old[0] in "-−" else ("+" if value >= 0 else ("−" if old[0] == "−" else "-"))
    elif value < 0:
        sign = "-"
    body = f"{abs(value):,}" if "," in old or (abs(value) >= 1000 and "," in old) else str(abs(value))
    return sign + body


def _num(s: str) -> int:
    return int(s.replace(",", "").replace("−", "-"))


def length_sites(lic: Path, skip, scope: str = "outward") -> tuple[list[dict], list[str]]:
    """草案の語数から導出する数を書いた場所の一覧 (460 (x) が照らし、sync_stated_counts.py --apply が書き換える)。

    照合と書き換えが別々の正規表現を持つと食い違うので、場所の一覧はここだけに置く (2026-11-15・1c の依頼: 試作の
    たびに 7 か所を手で直し、263→281 の誤りと 597 の直し忘れが同じ日に起きた)。scope="outward" は外向きの文書
    (B3 の見出し・SUBMISSION-MATERIALS の長さの行) だけ、"all" は草案冒頭の申告と CHANGELIST の語数の内訳と英文も含む。
    数え方: 題名から = 区切り線の後から END OF TERMS まで (prepare_version_freeze.size と同じ)、条文 = `1.` の見出し
    から END OF TERMS の手前まで。GPL-3.0 の数は reviewer-positions.md の表から読む。束の表の各行と冒頭の箇条の
    (+N words.) は判断の数なので場所に入れない。外向きの行は「N.M 草案は」から最初の日付つきの追記
    (**2026- / （2026-) の手前までを読み、後ろは当時の記録として読まない。ただし「条文では N 語長いまま」は
    現在形の主張なので行のどこでも読む。
    返り値: (場所の list, 読めないものの誤りの文)。場所は {path, line, start, end, old, new, what}。
    """
    drafts = [p for p in sorted(lic.glob("ACD-*-DRAFT.txt"))
              if "HAS BEEN FROZEN" not in p.read_text(encoding="utf-8").split("\n", 1)[0]]
    gpl = re.search(r"^\| GPL-3\.0 \| \*\*([\d,]+)\*\* \| \*\*([\d,]+)\*\* \|",
                    (lic / "ACD-1.0.reviewer-positions.md").read_text(encoding="utf-8"), re.M)
    if len(drafts) != 1 or not gpl:
        return [], [f"作業中の草案がちょうど 1 つでない ({[p.name for p in drafts]}) か、"
                    "reviewer-positions.md の GPL-3.0 の行 (題名から / 条文) を読めない"]
    dtext = drafts[0].read_text(encoding="utf-8")
    ver = re.match(r"ACD-(\d+\.\d+)-DRAFT", drafts[0].name).group(1)
    body = dtext.split(RULE, 1)[-1]
    end, sec1 = body.find("END OF TERMS"), re.search(r"^1\.\s", body, re.M)
    title = len(body.split())
    clauses = len(set(re.findall(r"^  (\d+\.\d+) ", body, re.M)))
    ops = len(body[sec1.start():end].split()) if sec1 and end > 0 else -1
    g_title, g_ops = (int(g.replace(",", "")) for g in gpl.groups())
    sites: list[dict] = []

    def add(path, ln, line, m, values, what):
        for gi, v in enumerate(values, 1):
            if v is not None and m.group(gi) is not None:
                sites.append({"path": path, "line": ln, "start": m.start(gi), "end": m.end(gi),
                              "old": m.group(gi), "new": _fmt(m.group(gi), v), "what": what})

    outward = [  # (正規表現, 値, 何の数か) —— 「N.M 草案は」から日付の手前まで
        (r"題名から(?:は)? ?([\d,]+) ?語", [title], "題名からの語数"),
        (r"GPL-3\.0[^。、]*?より ?([\d,]+) ?語短", [g_title - title], "題名からの GPL-3.0 との差"),
        (r"END OF TERMS\*? ?(?:の手前)?までが ?([\d,]+) ?語", [ops], "条文の語数"),
        (r"条文では ?([\d,]+) ?語長い(?!まま)", [ops - g_ops], "条文の GPL-3.0 との差"),
        (r"同じ数え方で [\d,]+ ?語・(\+[\d,]+)", [ops - g_ops], "条文の GPL-3.0 との差"),
    ]
    # 「確定した ACD-N.M は」の行は、その版の凍結した本文で測る (2026-11-16・50 の決め: 確定の日に B3 と SUBMISSION-MATERIALS の
    #   長さの行を「N.M 草案は」から「確定した ACD-N.M は」へ書き直す)。旧版は草案の名乗りだけを読んだので、書き直した日に
    #   照らす行が 0 になり「1 つも見つからない」で RED になった (確定の予行で実測)
    labels = [(f"{ver} 草案は", (title, ops), outward)]
    for fp in sorted(lic.glob("ACD-[0-9]*.[0-9]*.txt")):
        fv = re.match(r"ACD-(\d+\.\d+)\.txt$", fp.name)
        if not fv:
            continue
        fb = fp.read_text(encoding="utf-8").split(RULE, 1)[-1]
        fe, fs = fb.find("END OF TERMS"), re.search(r"^1\.\s", fb, re.M)
        ft, fo = len(fb.split()), (len(fb[fs.start():fe].split()) if fs and fe > 0 else -1)
        labels.append((f"確定した ACD-{fv.group(1)} は", (ft, fo), [
            (r"題名から(?:は)? ?([\d,]+) ?語", [ft], "題名からの語数 (確定した本文)"),
            (r"GPL-3\.0[^。、]*?より ?([\d,]+) ?語短", [g_title - ft], "題名からの GPL-3.0 との差 (確定した本文)"),
            (r"END OF TERMS\*? ?(?:の手前)?までが ?([\d,]+) ?語", [fo], "条文の語数 (確定した本文)"),
            (r"条文では ?([\d,]+) ?語長い(?!まま)", [fo - g_ops], "条文の GPL-3.0 との差 (確定した本文)"),
            (r"同じ数え方で [\d,]+ ?語・(\+[\d,]+)", [fo - g_ops], "条文の GPL-3.0 との差 (確定した本文)"),
        ]))
    for p in sorted(lic.glob("*.md")) + sorted((lic.parent / "docs/files/LICENSES").glob("*.md")):
        if skip(p.name) or "CLARITY-TRIAL" in p.name:
            continue
        for ln, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            for label, (_lt, lops), rxs in labels:
                if label not in line:
                    continue
                a = line.index(label)
                cut = re.search(r"\*\*20\d\d-\d\d-\d\d|（20\d\d-\d\d-\d\d", line[a:])
                b = a + cut.start() if cut else len(line)
                for rx, vals, what in rxs:
                    for m in re.compile(rx).finditer(line, a, b):
                        add(p, ln, line, m, vals, what)
                for m in re.finditer(r"条文では ?([\d,]+) ?語長いまま", line):
                    add(p, ln, line, m, [lops - g_ops], "条文の GPL-3.0 との差 (長いまま)")
                break
    if scope == "all":
        prev = None
        hdr = re.search(r"ACD-(\d+\.\d+): (\d+) words, (\d+) clauses\. This draft: (\d+) words, (\d+) clauses\.", dtext)
        if hdr and (lic / f"ACD-{hdr.group(1)}.txt").exists():
            pb = (lic / f"ACD-{hdr.group(1)}.txt").read_text(encoding="utf-8").split(RULE, 1)[-1]
            prev = (len(pb.split()), len(set(re.findall(r"^  (\d+\.\d+) ", pb, re.M))))
            ln = dtext[:hdr.start()].count("\n") + 1
            line = dtext.splitlines()[ln - 1]
            m = re.search(r"ACD-\d+\.\d+: (\d+) words, (\d+) clauses\. This draft: (\d+) words, (\d+) clauses\.", line)
            if m:
                add(drafts[0], ln, line, m, [prev[0], prev[1], title, clauses], "草案冒頭の語数と条数")
        o10 = (lic / "ACD-1.0.txt").read_text(encoding="utf-8").split(RULE, 1)[-1]
        w10 = (len(o10.split()), len(set(re.findall(r"^  (\d+\.\d+) ", o10, re.M))))
        cl = lic / f"ACD-{ver}-CHANGELIST.md"
        ctext = cl.read_text(encoding="utf-8") if cl.exists() else ""
        sec = ctext.split("\n## 語数の内訳", 1)[1].split("\n## ", 1)[0] if "\n## 語数の内訳" in ctext else ""
        bundles = {n.strip(): _num(v) for n, v in re.findall(r"^\| ([^|]+?) ?\| ([+−-]\d+) \|", sec, re.M) if n.strip() != "束"}
        for ln, line in enumerate(ctext.splitlines(), 1):
            m = re.search(r"\d+\.\d+ の ([\d,]+) 語から " + re.escape(ver) + r" 草案は ([+−-]\d+) 語", line)
            if m and prev:
                add(cl, ln, line, m, [prev[0], title - prev[0]], "前版の語数と差")
            m = re.search(r"1\.0 の ([\d,]+) 語から見ると (\d+) 語長い", line)
            if m:
                add(cl, ln, line, m, [w10[0], title - w10[0]], "1.0 の語数と差")
            m = re.search(r"（([^（）]+?)の (\d+) 束で ([+−-]\d+)）", line)
            if m and bundles:
                names = [n.strip() for n in re.split(r"、|，|,", m.group(1)) if n.strip()]
                picked = [k for k in bundles if any(k.startswith(n) for n in names)]
                if len(picked) == len(names):
                    sites.append({"path": cl, "line": ln, "start": m.start(3), "end": m.end(3), "old": m.group(3),
                                  "new": _fmt(m.group(3), sum(bundles[k] for k in picked)), "what": "名指した束の和"})
            m = re.search(r"([\d,]+) words from the title to \*END OF TERMS\* against 1\.0's ([\d,]+), in (\d+) clauses "
                          r"against (\d+)", line)
            if m:
                add(cl, ln, line, m, [title, w10[0], clauses, w10[1]], "英文の語数と条数")
    return sites, []


def apply_sites(sites: list[dict]) -> int:
    """場所の old を new へ書き換える (同じ行の中は右から)。書き換えた場所の数を返す。"""
    by_file: dict = {}
    for s in sites:
        if s["old"] != s["new"]:
            by_file.setdefault(s["path"], []).append(s)
    for path, ss in by_file.items():
        # file 全体の位置で持つ場所 ("abs") は先に後ろから、行の中の位置で持つ場所はその後に
        text = path.read_text(encoding="utf-8")
        for s in sorted((s for s in ss if s.get("abs")), key=lambda s: -s["start"]):
            assert text[s["start"]:s["end"]] == s["old"], (path, s)
            text = text[:s["start"]] + s["new"] + text[s["end"]:]
        lines = text.split("\n")
        for s in sorted((s for s in ss if not s.get("abs")), key=lambda s: (s["line"], -s["start"])):
            ln = lines[s["line"] - 1]
            assert ln[s["start"]:s["end"]] == s["old"], (path, s)
            lines[s["line"] - 1] = ln[:s["start"]] + s["new"] + ln[s["end"]:]
        path.write_text("\n".join(lines), encoding="utf-8")
    return sum(len(v) for v in by_file.values())


def draft_length_claims(lic: Path, skip) -> tuple[int, list[str]]:
    """460 (x): 外向きの文書が「いまの草案」の長さとして述べる数を、草案の実測と照らす (場所は length_sites)。

    B3 の見出しと SUBMISSION-MATERIALS の長さの行は現在形で語数と GPL-3.0 との差を述べるが、Check 468 が照らすのは
    草案冒頭の申告だけで、この行は誰も見ていなかった (2026-11-15・1c の T61/T62 の +18 語で 8 箇所が黙って古くなる
    ところだった)。英語の "N words from the title" は読まない —— 498 (j) が CHANGELIST では ADVISORY と決めている。
    返り値: (照らした箇所の数, 誤りの文の list)。直すには `python3 .github/scripts/sync_stated_counts.py --apply`。
    """
    sites, bad = length_sites(lic, skip, "outward")
    bad = [f"(x) {b}" for b in bad]
    for s in sites:
        if s["old"] != s["new"]:
            bad.append(f"(x) {s['path'].name}:{s['line']} の{s['what']} {s['old']} / 草案の実測から {s['new']} "
                       "(sync_stated_counts.py --apply で直る)")
    if not sites and not bad:
        bad.append("(x) 草案の長さを述べる行が 1 つも見つからない (B3 と SUBMISSION-MATERIALS の長さの行の形が"
                   "変わったなら本 face を直すこと —— 無いと黙る gate にしない)")
    return len(sites), bad


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


def errata_list_mismatch(pre: str, ver: str, errata: Path) -> list[str]:
    """468i: 草案冒頭の変更一覧と、errata の「N.M 草案で閉じた」の印の両向きの照合。

    順向き (2026-09-28): errata が「この草案で閉じた」とする番号が冒頭の一覧に無い —— E34 が 3 日間載っていなかった。
    冒頭は「a list with entries in it is the whole of the difference」と自分で宣言している。
    逆向き (2026-11-15・9b): 変更の箇条が「(errata E24)」と名乗る番号が、この草案で閉じた印を持たない —— 別の版で閉じた
    番号・存在しない番号・印の付け忘れ。どの変更がどの欠陥を閉じたかの記録が偽になる。「Still open in this draft」の行
    (E6 / E10) は 468e が見るので、逆向きは箇条の区間 (「Changes in this draft」から「This draft:」まで) だけを読む。
    """
    if not errata.exists():
        return []
    listed = set(re.findall(r"\bE\d+\b", pre))
    closed = set()
    for ln in errata.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*\*{0,2}(E\d+)\*{0,2}\s*\|", ln)
        if m and (ver + " 草案で閉じた") in ln:
            closed.add(m.group(1))
    bad = []
    miss = sorted(closed - listed, key=lambda e: int(e[1:]))
    if miss:
        bad.append(f"468i: errata が「{ver} 草案で閉じた」とする {miss} が冒頭の変更一覧に無い (冒頭は一覧が差分のすべてだと宣言している)")
    chg = pre.split("Changes in this draft", 1)[-1].split("This draft:", 1)[0]
    wrong = sorted(set(re.findall(r"\bE\d+\b", " ".join(chg.split()))) - closed, key=lambda e: int(e[1:]))
    if wrong:
        bad.append(f"468i: 変更の箇条が名乗る errata {wrong} が「{ver} 草案で閉じた」の印を持たない "
                   "(別の版で閉じた番号・存在しない番号・印の付け忘れ)")
    return bad


def materials_0d_mismatches(materials: str, clauses: dict) -> tuple[int, list[str]]:
    """468 (§0d): 提出の材料 §0d の「狭めたと読まれうる箇所」の表の 1 列目が述べる草案の状態を、草案の本文と照らす。

    表の行は「§9.2 の第 3 文から *"A"* と *"B"* を外し、*"C"* を足した」「§8.1 は *"derived from"*」の形で草案の今の状態を
    前提にしているが、草案が変わっても何も鳴らなかった (50 の提案・2026-11-15。同じ日に §9.2 の行を 1c の指摘で手で直した)。
    「を外」が続く引用は、その条に無いこと。「を足」が続く引用と「§N.M は」の後の引用は、その条に在ること。条は引用の前の
    最も近い § (「§8.4・§6.4 は」なら両方)。動詞の読めない引用は照らさない (照らした数は返り値に出る)。
    返り値: (照らした引用の数, 誤りの文の list)。表が読めなければ誤り。
    """
    sec = re.search(r"^## 0d\..*?(?=^## )", materials, re.M | re.S)
    if not sec:
        return 0, ["468 (§0d): SUBMISSION-MATERIALS.md の「## 0d.」の節を読めない"]
    norm = {k: " ".join(v.split()) for k, v in clauses.items()}
    n, bad = 0, []
    for line in sec.group(0).split("\n"):
        if not line.startswith("| ") or line.startswith(("| もの", "| 箇所", "|---")):
            continue
        c0 = re.split(r"(?<!\\)\|", line.strip().strip("|"))[0]
        for m in re.finditer(r'\*"([^"]+)"\*', c0):
            rest = re.sub(r'^(?:\s*(?:と|、|・)\s*\*"[^"]+"\*)+', "", c0[m.end():])
            before = c0[:m.start()]
            if re.match(r"\s*を外", rest):
                want = False
            elif re.match(r"\s*を足", rest):
                want = True
            elif re.search(r"は\s*$", before):
                want = True
            else:
                continue
            grp = re.search(r"((?:§\d+\.\d+(?:\([a-z]\))?[・、 ]*)+)[^§]*$", before)
            keys = re.findall(r"§(\d+\.\d+)", grp.group(1)) if grp else []
            if want and re.search(r"は\s*$", before):
                keys = re.findall(r"§(\d+\.\d+)", re.search(r"((?:§\d+\.\d+[・、 ]*)+)は\s*$", before).group(1)) if re.search(r"((?:§\d+\.\d+[・、 ]*)+)は\s*$", before) else keys[-1:]
            else:
                keys = keys[-1:]
            for k in keys:
                n += 1
                if (m.group(1) in norm.get(k, "")) != want:
                    bad.append(f"468 (§0d): 材料 §0d の表が §{k} に *\"{m.group(1)}\"* が{'在る' if want else '無い'}と前提にしているが、"
                               f"いまの草案では{'無い' if want else '在る'} (草案が変わったなら表の行を読み直す)")
    return n, bad


def draft_has_changes(draft_text: str) -> bool:
    """作業中の草案の冒頭の変更一覧に、要約の行 (「ACD-N.M: N words, … This draft: …」) 以外の箇条が在るか。

    版を確定した直後の新しい草案は変更が 0 件で、一覧は要約の 1 行だけになる (2026-11-15 の確定の試走)。その状態で
    「主表を読めない」(468x)・「語数の内訳を読めない」(498 (k)) を RED にすると、確定の日の CI が理由なく止まる。
    """
    pre = draft_text.split(RULE, 1)[0]
    chg = pre.split("Changes in this draft", 1)[-1].split("Still open", 1)[0]
    return bool(re.search(r"\n    \* (?!ACD-\d+\.\d+: )", chg))
