#!/usr/bin/env python3
"""make_redline.py — ACD の 2 つの版の、条ごとの語の差 (redline) を 80 桁の plain text で出す。

**なぜ在るか (2026-11-15・50 の依頼)**: 審査者は新しいライセンスに「既存のものとの差」を求める ——
Chestek 氏 (2026-01-23) と Sado 氏 (2026-01-24) は redline か *"innovations only"* の抜粋を求めた
(`ACD-1.0.review-readings.md`)。計画の段 6b は、本申請の前に 1.4 の新しい語を 1.0 との差としてオーナーが
license-discuss へ出す。差を手で作ると、条の対応を取り違え (1.0 と 1.1 以降は条番号がずれる) 語を落とす。

**出すもの**: 新しい版の条の順に、条ごとに (a) 変わらない / (b) 変わった (語の差を `[-旧-]{+新+}` で) /
(c) 新設 / (d) 前の版にだけ在る、を出す。前文と節の見出しも同じ扱い。各行は 80 桁以内、ASCII のまま。
冒頭に 2 つの入力の file 名・sha256・語数を書く (どの本文の差かを読み手が確かめられるように)。

**条の対応**: 1.0 → 1.1 は条番号が並べ替えられた。対応は `LICENSES/ACD-1.1-CHANGELIST.md` §0.5 の表を読む
(確定版に当て直した表・単一の出所。この道具に写さない)。1.1 以降は条番号が同じ (草案の冒頭が
"Clause numbers follow ACD-1.3 (which follows ACD-1.1)" と述べる)。1.0 を旧にしたときは表を、
それ以外は同じ番号を当てる。表の行が読めなければ止まる (黙って同じ番号を当てない)。
表が結ばなかった条は、同じ節の結ばれていない条のうち語の並びが最も近いもの (比 0.5 以上) へ結ぶ (2026-11-23・`match_leftovers`)。

**測っていないもの**: 法的効果。語の差は効果の差の証拠ではない。版番号と識別子の差も、そのまま差として出す。

使い方 (CI では回さない。出力は投稿の日・申請の日に作り、そのとき使った commit を書き添える):
    python3 .github/scripts/make_redline.py LICENSES/ACD-1.0.txt LICENSES/ACD-1.4-DRAFT.txt > redline.txt
    python3 .github/scripts/make_redline.py --changed-only LICENSES/ACD-1.3.txt LICENSES/ACD-1.4-DRAFT.txt
    python3 .github/scripts/make_redline.py --changed-only --context 8 LICENSES/ACD-1.0.txt LICENSES/ACD-1.4-DRAFT.txt
        # 変わった語の前後 8 語だけを残し、間を "..." にする (list に貼れる長さへ・2026-11-15。全文の redline は 1.0→1.4 で
        #   5,702 語あり、本体とほぼ同じ長さだった)
    python3 .github/scripts/make_redline.py --coverage LICENSES/ACD-1.3.txt LICENSES/ACD-1.4-DRAFT.txt
        # 段 7 の「差分の完全性」(2026-11-20・50 の依頼 (3)): 条ごとの語の差の塊 (hunk) それぞれについて、変更の一覧
        #   (CHANGES-ACD-N.M.txt か草案の冒頭の一覧) のどの箇条の引用が、その塊の新しい語 (無ければ消えた語) を覆うかを出す。
        #   覆う箇条は、その条を名指し (Section N.M・前文は Preamble)、引用 ("…") の中にその塊の語の連なりを持つもの。
        #   どの箇条にも覆われない塊は「述べられない変更」の候補 (読む人が決める・語の差は効果の差ではない)
"""
from __future__ import annotations

import difflib
import hashlib
import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RULE = "-" * 80
CLAUSE = re.compile(r"^  (\d+\.\d+)\s+(.*?)(?=^  \d+\.\d+\s|^\d+\.\s|^END OF TERMS|\Z)", re.M | re.S)
HEAD = re.compile(r"^(\d+)\.\s+(\S.*)$", re.M)
MAP_TABLE = ROOT / "LICENSES" / "ACD-1.1-CHANGELIST.md"


def parts(text: str) -> dict[str, str]:
    """{key: 空白を正規化した本文}。key は "preamble" / "head N" / "N.M"。区切り線より上 (草案の注記) は読まない。"""
    body = text.split(RULE, 1)[1] if RULE in text else text
    end = body.find("END OF TERMS")
    body = body[:end] if end >= 0 else body
    out: dict[str, str] = {}
    pre = re.search(r"^PREAMBLE.*?$(.*?)(?=^1\.\s)", body, re.M | re.S)
    if pre:
        out["preamble"] = " ".join(pre.group(1).split())
    for m in HEAD.finditer(body):
        out[f"head {m.group(1)}"] = " ".join(m.group(2).split())
    for m in CLAUSE.finditer(body):
        out[m.group(1)] = " ".join(m.group(2).split())
    return out


def version_of(path: Path, text: str) -> str:
    m = re.search(r"Short identifier: ACD-(\d+\.\d+)", text)
    if not m:
        raise SystemExit(f"ERROR: {path} に Short identifier が無い")
    return m.group(1)


def map_from_10() -> dict[str, str | None]:
    """1.0 の条番号 → 1.1 以降の条番号 (削除は None)。表に無い番号は同じ番号。"""
    text = MAP_TABLE.read_text(encoding="utf-8")
    sec = text.split("## 0.5 ", 1)[1].split("\n## ", 1)[0] if "## 0.5 " in text else ""
    rows = [r for r in sec.split("\n") if r.startswith("|") and not r.startswith(("|---", "| 1.0 |"))]
    if not rows:
        raise SystemExit(f"ERROR: {MAP_TABLE.name} §0.5 の対応表を読めない (黙って同じ番号を当てない)")
    m: dict[str, str | None] = {}
    for r in rows:
        cells = [c.strip().strip("*").strip() for c in r.strip().strip("|").split("|")]
        old = re.findall(r"\d+\.\d+", cells[0])
        new = re.findall(r"\d+\.\d+", cells[1])
        if not old:
            continue  # 新設 (1.0 に無い)
        for o in old:
            m[o] = new[0] if new and len(old) == 1 else None
    return m


TEXT_MATCH_MIN = 0.5
MOVED_TABLE = ROOT / "LICENSES" / "ACD-1.4-CHANGELIST.md"  # 「条項の対応表（1.0 → 1.4）」の §15・§16 の表 (d7)


def moved_from_10() -> dict[str, tuple[str, str]]:
    """1.0 の条で、中身が 1.4 の別の条の一部へ移ったもの {1.0 の番号: (1.4 の番号, "the last sentence" か "")}。

    2026-11-24 (5e の案): redline は 1.0 §15.5 と §16.5 を「not in ACD-1.4」とだけ出し、list の審査者には不行使の規則と翻訳の
    扱いが消えたように読めた。語の近さでは 1.0 §15.5 → 1.4 §2.2 (0.36) と誤った組 1.0 §15.6 → 1.4 §11.1 (0.36) を分けられない
    ので、d7 が 1.0 と 1.4 の凍結した本文から作った対応表の「§X の末文」「§X の中」の行を読む。表が読めなければ空 (行き先を出さない)。
    """
    if not MOVED_TABLE.exists():
        return {}
    sec = MOVED_TABLE.read_text(encoding="utf-8").split("## 条項の対応表（1.0 → 1.4）", 1)
    out: dict[str, tuple[str, str]] = {}
    for row in (sec[1] if len(sec) > 1 else "").splitlines():
        m = re.match(r"^\| §(\d+\.\d+) \|[^|]*\| §(\d+\.\d+) ?の(末文|中) \|", row)
        if m:
            out[m.group(1)] = (m.group(2), "the last sentence of " if m.group(3) == "末文" else "")
    return out


def match_leftovers(A: dict[str, str], B: dict[str, str], to_new: dict[str, str | None]) -> dict[str, tuple[str, float]]:
    """表が結ばなかった 1.0 の条を、同じ節の結ばれていない新しい条のうち語の並びが最も近いものへ結ぶ (比 TEXT_MATCH_MIN 以上)。

    2026-11-23 (5e の報告・d7 の全文照合): 表は 1.0 → 1.1 の対応で、1.1 で消えて 1.2 / 1.3 で戻った条を追わない。1.0 §15.3
    (起草者不利の解釈の排除) は 1.4 §15.6 と字句同一 (比 1.00)、1.0 §15.2 (単数と複数) は 1.4 §15.5 とほぼ同じ (0.95) なのに、
    「新設」と「削除」に割れ、要約の new / removed が 2 件ずつ多かった。オーナーが list に出す材料なので、審査者には
    「起草者不利の規則を消して足し直した」と読める。同じ節の中だけで結ぶのは、節をまたぐ偶然の近さを避けるため。
    返り値: {旧の番号: (新の番号, 比)}。
    """
    import difflib
    clause = re.compile(r"\d+\.\d+")
    used = {v for v in to_new.values() if v and v in B}
    old_left = [k for k in A if clause.fullmatch(k) and to_new.get(k) not in B]
    new_left = [k for k in B if clause.fullmatch(k) and k not in used]
    pairs = sorted(((difflib.SequenceMatcher(None, A[o].split(), B[n].split()).ratio(), o, n)
                    for o in old_left for n in new_left if o.split(".")[0] == n.split(".")[0]), reverse=True)
    out: dict[str, tuple[str, float]] = {}
    taken: set[str] = set()
    for r, o, n in pairs:
        if r >= TEXT_MATCH_MIN and o not in out and n not in taken:
            out[o] = (n, r)
            taken.add(n)
    return out


def wdiff(a: str, b: str, context: int | None = None) -> str:
    """語の差を [-旧-]{+新+} で。context を与えると、変わらない語の連なりは前後 context 語だけを残し、間を " ... " にする (出力は ASCII のまま)。"""
    aw, bw = a.split(), b.split()
    out = []
    ops = difflib.SequenceMatcher(a=aw, b=bw, autojunk=False).get_opcodes()
    for n, (op, i1, i2, j1, j2) in enumerate(ops):
        if op == "equal":
            run = aw[i1:i2]
            if context is not None and len(run) > 2 * context + 1:
                head = run[:context] if n > 0 else []
                tail = run[-context:] if n < len(ops) - 1 else []
                out.extend(head + ["..."] + tail)
            else:
                out.extend(run)
            continue
        if i2 > i1:
            out.append("[-" + " ".join(aw[i1:i2]) + "-]")
        if j2 > j1:
            out.append("{+" + " ".join(bw[j1:j2]) + "+}")
    return " ".join(out)


def fill(text: str, indent: str = "    ") -> str:
    return textwrap.fill(text, width=80, initial_indent=indent, subsequent_indent=indent,
                         break_long_words=False, break_on_hyphens=False)


def label(key: str) -> str:
    return {"preamble": "Preamble"}.get(key, f"Heading of Section {key[5:]}" if key.startswith("head ") else f"Section {key}")


def _words(s: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9']+", s.lower())]


def coverage(A: dict[str, str], B: dict[str, str], bullets: list[str]) -> list[tuple[str, str, str, str]]:
    """条ごとの差の塊それぞれに、覆う箇条を当てる。返り値: [(条, 塊の短い表示, 当たり方, 箇条の頭)]。当たり方は quote (その条を名指す
    箇条の引用が塊の語の 3 語の連なりを持つ) / named (条を名指す箇条は在るが、引用は塊を覆わない —— 言い換えで述べた変更) / none
    (どの箇条もその条を名指さない —— 述べられない変更)。"""
    named = []
    for b in bullets:
        keys = set(re.findall(r"Sections? (\d+\.\d+)", b)) | ({"preamble"} if re.search(r"\bPreamble\b", b) else set())
        keys |= {f"head {n}" for n in re.findall(r"[Hh]eading of Section (\d+)\b", b)}  # 節の見出し ("The heading of Section 11 …")
        for rng in re.finditer(r"Sections (\d+)\.(\d+) to (\d+)\.(\d+)", b):
            if rng.group(1) == rng.group(3):
                keys |= {f"{rng.group(1)}.{i}" for i in range(int(rng.group(2)), int(rng.group(4)) + 1)}
        quotes = " | ".join(" ".join(_words(q)) for q in re.findall(r'"([^"]+)"', b))
        named.append((keys, quotes, b))
    out = []
    for key in B:
        if key not in A or A[key] == B[key]:
            continue
        aw, bw = A[key].split(), B[key].split()
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=aw, b=bw, autojunk=False).get_opcodes():
            if op == "equal":
                continue
            pw = _words(" ".join(bw[j1:j2])) or _words(" ".join(aw[i1:i2]))
            # 塊の語の 3 語の連なり (3 語に満たなければ塊の全部) のどれかが、その条を名指す箇条の引用の中に在れば「引用で覆う」
            grams = {" ".join(pw[i:i + 3]) for i in range(max(1, len(pw) - 2))} if pw else set()
            hit = next((b for keys, q, b in named if key in keys and any(g and g in q for g in grams)), "")
            level = "quote" if hit else ("named" if any(key in keys for keys, _q, _b in named) else "none")
            if not hit and level == "named":
                hit = next(b for keys, _q, b in named if key in keys)
            show = (f"[-{' '.join(aw[i1:i2])[:40]}-]" if i2 > i1 else "") + (f"{{+{' '.join(bw[j1:j2])[:40]}+}}" if j2 > j1 else "")
            out.append((key, show, level, hit[:70]))
    return out


def main(argv: list[str]) -> int:
    if "--coverage" in argv:
        args = [a for a in argv if not a.startswith("--")]
        pa, pb = Path(args[0]), Path(args[1])
        ta, tb = pa.read_text(encoding="utf-8"), pb.read_text(encoding="utf-8")
        ch = pb.with_name("CHANGES-" + pb.name.replace("-DRAFT.txt", ".txt"))
        src = ch.read_text(encoding="utf-8") if ch.exists() else tb.split(RULE, 1)[0]
        lst = src.split("Changes in this draft", 1)[-1]
        bullets = [" ".join(x.split()) for x in re.split(r"\n    \* ", lst)[1:]]
        rows = coverage(parts(ta), parts(tb), bullets)
        n = {lv: sum(1 for r in rows if r[2] == lv) for lv in ("quote", "named", "none")}
        print(f"Coverage: {len(rows)} hunks in changed parts of {pb.name} against {pa.name}: {n['quote']} covered by a quote in a "
              f"bullet that names the clause, {n['named']} in a clause a bullet names but not by its quotes (described in other "
              f"words), {n['none']} in a clause no bullet names.")
        for key, show, lv, hit in rows:
            if lv != "quote" or "--all" in argv:
                print(f"  [{lv}] {label(key)}: {show}  <-  {hit or '-'}")
        return 1 if n["none"] else 0
    changed_only = "--changed-only" in argv
    context = int(argv[argv.index("--context") + 1]) if "--context" in argv else None
    args = [a for a in argv if not a.startswith("--") and not (context is not None and a == str(context))]
    if len(args) != 2 or "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0 if ("-h" in argv or "--help" in argv) else 2
    pa, pb = Path(args[0]), Path(args[1])
    ta, tb = pa.read_text(encoding="utf-8"), pb.read_text(encoding="utf-8")
    va, vb = version_of(pa, ta), version_of(pb, tb)
    # 述べ直した版 (CLAUSE-MAP-x-y.tsv が間に在る) をまたぐ差は、同じ番号を当てると別の条どうしを並べる。1 条が複数の条へ分かれ、
    #   複数の条が 1 条に集まるので、条ごとの語の差は成り立たない。黙って誤った差を出さず止まる (2026-11-24・議題 16)
    vk = lambda v: tuple(int(x) for x in re.findall(r"\d+", v))
    for cm in sorted(pb.resolve().parent.glob("CLAUSE-MAP-*-*.tsv")):
        m = re.match(r"CLAUSE-MAP-(\d+\.\d+)-(\d+\.\d+)\.tsv$", cm.name)
        if m and vk(va) <= vk(m.group(1)) and vk(m.group(2)) <= vk(vb):
            print(f"ACD-{m.group(2)} restates ACD-{m.group(1)} and renumbers its clauses, so a clause-by-clause redline from ACD-{va} to "
                  f"ACD-{vb} would set different clauses side by side. Use the full text, CHANGES-ACD-{m.group(2)}.txt (what differs in "
                  f"effect) and {cm.name} (where each clause went).", file=sys.stderr)
            return 2
    A, B = parts(ta), parts(tb)
    m10 = map_from_10() if va == "1.0" and vb != "1.0" else {}
    to_new = {k: (m10.get(k, k) if re.fullmatch(r"\d+\.\d+", k) else k) for k in A}
    by_text = match_leftovers(A, B, to_new) if m10 else {}
    to_new.update({o: nk for o, (nk, _r) in by_text.items()})
    from_old = {v: k for k, v in to_new.items() if v}
    wa = len((ta.split(RULE, 1)[1] if RULE in ta else ta).split())
    wb = len((tb.split(RULE, 1)[1] if RULE in tb else tb).split())
    print(f"Redline: ACD-{va} -> ACD-{vb}, clause by clause, in the order of ACD-{vb}.")
    print(f"  Old: {pa.name}  sha256 {hashlib.sha256(ta.encode()).hexdigest()[:16]}  {wa} words")
    print(f"  New: {pb.name}  sha256 {hashlib.sha256(tb.encode()).hexdigest()[:16]}  {wb} words")
    print("  [-words-] are in the old text only; {+words+} are in the new text only.")
    if m10:
        print(f"  Clause numbers of ACD-1.0 are matched to ACD-{vb} by the table in")
        print("  LICENSES/ACD-1.1-CHANGELIST.md section 0.5; where a number moved, the")
        print("  old number is shown in brackets. A clause the table leaves unmatched is")
        print("  matched by text to the most similar unmatched clause of the same section,")
        print(f"  if the similarity of their words is at least {TEXT_MATCH_MIN}; the bracket")
        print("  then says \"matched by text\" and gives the similarity.")
    print("  Word differences are not differences of legal effect.")
    print()
    counts = {"unchanged": 0, "changed": 0, "new": 0, "removed": 0}  # new = 旧版に無い / removed = 新版に無い
    for key in B:
        old = from_old.get(key)
        via = next((f", matched by text {r:.2f}" for o2, (nk, r) in by_text.items() if nk == key), "")
        tag = label(key) + (f" [ACD-{va} {old}{via}]" if old and (old != key or via) else "")
        if old is None or old not in A:
            counts["new"] += 1
            # 番号の使い回し (2026-11-15・50 の検証): 1.0 の §15.5 / §15.6 は 1.1 で消え、1.2 / 1.3 が同じ番号に別の条を
            #   置いた。「new」とだけ書くと、旧版の同じ番号の条が消えて新しく出たのか取り違える
            reused = f" (ACD-{va} also has a Section {key}, with other content; see below)" if key in A else ""
            print(fill(f"{tag}: not in ACD-{va}{reused}", indent=""))
            print(fill("{+" + B[key] + "+}"))
            print()
        elif A[old] == B[key]:
            counts["unchanged"] += 1
            if not changed_only:
                print(f"{tag}: unchanged")
                print()
        else:
            counts["changed"] += 1
            print(f"{tag}: changed")
            print(fill(wdiff(A[old], B[key], context)))
            print()
    moved = moved_from_10() if m10 and vb == "1.4" else {}
    for key in A:
        if to_new.get(key) not in B:
            counts["removed"] += 1
            now = f" (ACD-{vb} uses the number {key} for other content)" if key in B else ""
            print(fill(f"{label(key)} of ACD-{va}: not in ACD-{vb}{now}", indent=""))
            if key in moved:
                counts["moved into another section"] = counts.get("moved into another section", 0) + 1
                print(fill(f"Its content is now in {moved[key][1]}Section {moved[key][0]} of ACD-{vb} (by the table in "
                           f"LICENSES/{MOVED_TABLE.name}, section on clause numbers 1.0 to 1.4).", indent=""))
            print(fill("[-" + A[key] + "-]"))
            print()
    print(fill("Summary: " + ", ".join(f"{v} {k}" for k, v in counts.items() if k != "moved into another section")
               + (f" (of the removed, {counts['moved into another section']} moved into another section)"
                  if counts.get("moved into another section") else "") + ".", indent=""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
