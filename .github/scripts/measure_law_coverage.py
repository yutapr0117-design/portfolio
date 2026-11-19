#!/usr/bin/env python3
"""measure_law_coverage.py — 1.4 草案の条ごとに、その読みが頼る法令の写し (rounds/ の *-snapshot.txt) を結ぶ対応表 (2026-11-20・5 人の分担の 9b の (2))。

**なぜ在るか**: 法令の一次資料を 5 人で分担して読む (オーナーの依頼・2026-11-20)。読んだ写しが草案のどの条に当たったか、§18 の
「頼っている法の命題」の行がどの写しを引き、どれがまだ「未取得」と書いているかを、条ごとに数で言えないと、分担の残りが見えない。

**数え方**:
  - §18 (THIRD の「## 18.」の節) の行 —— 表の行 (`| §x.y …`) と箇条の行 (`- §x.y | 命題: …`)。行の頭の §x.y を条とする。
    行が引く写し (`…-snapshot.txt` の名) と、行に残る「未取得」の句を数える。
  - 写しの側 —— rounds/ の `*-snapshot.txt`。新しい形 (add_law_snapshot.py) はヘッダの `Applied to: … Sections 2.2, 4.1` を、
    古い形は §18 の行と jurisdictions*.md がその写しの名を引く所の条を、写しが当たる条とする。
  - 「未取得」が残るのに、行が名指す法令の写しが rounds/ に在るもの (取った後で行を直していない) は、drift として出す。
出力: 条ごとの表 (--table)、要約 (既定)。

使い方:
    python3 .github/scripts/measure_law_coverage.py          # 要約
    python3 .github/scripts/measure_law_coverage.py --table  # 条ごとの対応表 (Markdown)
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
L = ROOT / "LICENSES"
SNAP = re.compile(r"(\d{4}-\d{2}-\d{2}-[a-z0-9-]+-snapshot\.txt)")
# 法令・判例の出所 (OSI の頁や FAQ の写しは法源でないので、当たっていない写しの数に入れない)
LAW_HOST = re.compile(r"https?://[^/\s]*(?:gesetze-im-internet|legislation\.gov\.uk|e-gov\.go\.jp|legifrance|law\.cornell|uscode\.house|"
                      r"govinfo|eur-lex|wipo\.int|caselaw\.|courtlistener|lexaris|gesetze\.co/urteile|laws-lois\.justice)")


def ckey(c: str) -> tuple:
    return tuple(int(x) for x in re.findall(r"\d+", c))


def draft_clauses() -> list[str]:
    d = next(p for p in sorted(L.glob("ACD-1.*-DRAFT.txt")) if "HAS BEEN FROZEN" not in p.read_text(encoding="utf-8").split("\n", 1)[0])
    body = d.read_text(encoding="utf-8").split("-" * 80, 1)[-1]
    return sorted(set(re.findall(r"^  (\d+\.\d+) ", body, re.M)), key=ckey)


def s18_rows() -> list[tuple[str, str]]:
    th = sorted(L.glob("ACD-1.*-THIRD-CLARITY-TRIAL.md"))[-1].read_text(encoding="utf-8")
    m = re.search(r"^## (?:§)?18[ .].*?(?=^## (?:§)?\d+[ .]|\Z)", th, re.M | re.S)
    out = []
    for line in (m.group(0) if m else "").split("\n"):
        h = re.match(r"^(?:\| |- )§(\d+\.\d+)", line)
        if h:
            out.append((h.group(1), line))
    return out


def snapshots() -> dict[str, set[str]]:
    """写しの名 → 当たる条の集合 (ヘッダの Applied to か、§18・jurisdictions の引用から)。"""
    snaps = {p.name: set() for p in sorted((L / "rounds").glob("*-snapshot.txt"))}
    for name in snaps:
        head = (L / "rounds" / name).read_text(encoding="utf-8")[:2000]
        a = re.search(r"^Applied to: .*?Sections? ([\d., ]+)$", head, re.M)
        if a:
            snaps[name] |= set(re.findall(r"\d+\.\d+", a.group(1)))
    for c, line in s18_rows():
        for s in SNAP.findall(line):
            if s in snaps:
                snaps[s].add(c)
    for f in sorted(L.glob("ACD-1.*.jurisdictions*.md")):
        for para in f.read_text(encoding="utf-8").split("\n\n"):
            for s in SNAP.findall(para):
                if s in snaps:
                    snaps[s] |= {x for x in re.findall(r"§(\d+\.\d+)", para)}
    return snaps


def unapplied() -> list[tuple[str, str]]:
    """写しのヘッダの Applied to が挙げる条のうち、§18 のその条の行も、jurisdictions*.md の段 (写しの名とその §x.y を持つ段) も、§19 の行も
    その写しを引いていない組 (写し, 条) (2026-11-20)。「取ったが、その条の読みにまだ当てていない」を数える。"""
    cited = {}
    for c, line in s18_rows():
        for s in SNAP.findall(line):
            cited.setdefault(s, set()).add(c)
    for f in sorted(L.glob("ACD-1.*.jurisdictions*.md")):
        for para in f.read_text(encoding="utf-8").split("\n\n"):
            for s in SNAP.findall(para):
                cited.setdefault(s, set()).update(re.findall(r"§(\d+\.\d+)", para))
    # §19 (一意に定める記録) の行が写しを引いて読みを書いた条も、当てたと数える (2f の §1.5 と DSM 指令 15 条の行など)
    for f in sorted(L.glob("ACD-1.*-UNIQUE-READING.md"))[-1:]:
        for line in f.read_text(encoding="utf-8").splitlines():
            h = re.match(r"^- (§[^|]+?) \|", line)
            if h:
                for s in SNAP.findall(line):
                    cited.setdefault(s, set()).update(re.findall(r"(\d+\.\d+)", h.group(1)))
    out = []
    for p in sorted((L / "rounds").glob("*-snapshot.txt")):
        a = re.search(r"^Applied to: .*?Sections? ([\d., ]+)$", p.read_text(encoding="utf-8")[:2000], re.M)
        for c in sorted(set(re.findall(r"\d+\.\d+", a.group(1))) if a else (), key=ckey):
            if c not in cited.get(p.name, set()):
                out.append((p.name, c))
    return out


def main(argv: list[str]) -> int:
    clauses = draft_clauses()
    rows = s18_rows()
    snaps = snapshots()
    by_clause = defaultdict(lambda: {"rows": 0, "unfetched": [], "snaps": set()})
    for c, line in rows:
        b = by_clause[c]
        b["rows"] += 1
        for mu in re.finditer(r"[^（(、。；|]{0,40}未取得", line):
            # 「取得経路が閉じている（403 など）」と書いた句は経路待ちとして印を付ける (2026-11-20)
            mark = "［経路待ち］" if re.search(r"取得経路|403|404", line[mu.end():mu.end() + 60]) else ""
            b["unfetched"].append(mu.group(0).strip(" ・（(") + mark)
        b["snaps"] |= {s for s in SNAP.findall(line) if s in snaps}
    for s, cs in snaps.items():
        for c in cs:
            by_clause[c]["snaps"].add(s)
    law = {s for s in snaps if LAW_HOST.search((L / "rounds" / s).read_text(encoding="utf-8")[:1500])}
    orphan = [s for s, cs in snaps.items() if not cs and s in law]
    unf = [(c, u) for c in sorted(by_clause, key=ckey) for u in by_clause[c]["unfetched"]]
    with_snap = [c for c in clauses if by_clause[c]["snaps"]]
    with_row = [c for c in clauses if by_clause[c]["rows"]]
    if "--table" in argv:
        print("| 条 | §18 の行 | 当たる写し | 未取得と書かれた法源 |\n| :-- | --: | :-- | :-- |")
        for c in clauses:
            b = by_clause[c]
            print(f"| §{c} | {b['rows']} | {'<br>'.join(sorted(b['snaps'])) or '—'} | {'；'.join(b['unfetched']) or '—'} |")
        return 0
    print(f"# 法源の対応（草案 {len(clauses)} 条）: §18 の行を持つ条 {len(with_row)}・写しが当たる条 {len(with_snap)}（rounds/ の写し {len(snaps)} 本・うち法令と判例 {len(law)} 本）")
    waiting = sum(1 for _, u in unf if u.endswith("［経路待ち］"))
    print(f"# §18 の行 {len(rows)} のうち写しを引く行 {sum(1 for _, l in rows if SNAP.search(l))}・「未取得」の句 {len(unf)}"
          f"（うち取得経路が閉じている {waiting}）: "
          + "；".join(f"§{c} {u}" for c, u in unf))
    un = unapplied()
    print(f"# 写しのヘッダが挙げる条のうち、§18 の行にも jurisdictions の段にも §19 の行にも引かれていない組 {len(un)}（取ったが、その条の読みに"
          f"まだ当てていない）: " + "；".join(f"§{c} ← {s[11:50]}" for s, c in un))
    print(f"# 草案のどの条にも当たっていない法令・判例の写し {len(orphan)}（§18・jurisdictions が名を引かず、ヘッダに Applied to も無い）: " + ", ".join(orphan))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
