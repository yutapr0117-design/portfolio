#!/usr/bin/env python3
"""measure_patent_reach.py — B10 の立証 (gap-measurements.md §1.133) を、審査者が自分で再現するための道具。

**なぜ在るか (2026-11-04)**: §1.133 は「OSI 承認済み・非 deprecated の全ライセンスのうち、作品を超える対象への
特許許諾と、条件の不在を同時に持つものは 0 本」と述べる。**測れると言う主張には、実際に走るコマンドを添える**
(measure_gap_claim.py が在るのと同じ理由・#122 / #123 の族)。この道具はその 0 を、原文の逐語つきで出し直す。

**測っているもの**:
  1. gap-census.md の全数表から、特許許諾の範囲が作品を超える (`S2` / `S3`) 本を拾う
  2. それぞれの SPDX 原文から、**条件** (notice 等の義務) と **終了** (terminate / ends) の文を逐語で出す
  3. 「作品を超える特許許諾 ∧ 条件が 1 つも無い」本の数を出す

**測っていないもの (重要)**:
  - census の範囲の分類 (`S1` = 作品・寄与に閉じる) は**読みの判定**で、この道具は検証しない。
    `S1` の本が実はモデルに届くと読めるなら、結論は変わりうる (§1.133「確立しないこと 2」)。
  - 条件・終了の検出は正規表現で、**見つけた文を示す**ことまでしかしない。見つからないことは「無い」の証明ではない。
  - 法的な効果。OSI の判断。

使い方:
    python3 .github/scripts/generate_gap_census.py --fetch   # SPDX の原文を取得 (ネットワーク要・一度だけ)
    python3 .github/scripts/generate_gap_census.py --check   # census が取得した原文から再現するか
    python3 .github/scripts/measure_patent_reach.py          # 本道具
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CACHE = Path(os.environ.get("GAP_CENSUS_CACHE", "/tmp/gap-census-cache"))
CENSUS = ROOT / "LICENSES" / "ACD-1.0.gap-census.md"

# 条件は優先順に探す: notice 等の具体的な義務 → 条件付きの許諾の言い回し → 汎用の must。
# 汎用の "you must" を先にすると、BlueOak の受諾の文 ("you must agree to its rules") を拾い、
# 立証の根拠として示すべき notice の義務を出さない (2026-11-04 の初版で実際にそうなった)。
COND = [re.compile(p + r"[^.]{0,160}", re.I) for p in (
    r"must (?:ensure|be included|retain|include|reproduce)",
    r"subject to the following conditions?",
    r"provided that",
    r"on condition that",
    r"you must",
)]
TERM = re.compile(r"(shall terminate|license ends immediately|terminated by the Licensor for cause|"
                  r"will terminate|terminates? automatically|rights .{0,40} terminate)[^.]{0,120}", re.I)


def main() -> int:
    if not (CACHE / "_meta.json").exists():
        print(f"SPDX の原文が無い: {CACHE} —— generate_gap_census.py --fetch を先に走らせる")
        return 2
    meta = json.loads((CACHE / "_meta.json").read_text(encoding="utf-8"))
    rows = [ln for ln in CENSUS.read_text(encoding="utf-8").splitlines() if ln.startswith("| `")]
    beyond = []
    for ln in rows:
        cells = [c.strip() for c in ln.split("|")]
        if len(cells) > 5 and cells[5] in ("S2", "S3"):
            beyond.append(cells[1].strip("`"))
    print(f"# SPDX licenseListVersion {meta.get('licenseListVersion')} / releaseDate {meta.get('releaseDate')} / "
          f"取得 {meta.get('fetched_at')} / 承認済み非 deprecated {meta.get('approved_nondeprecated')} 本")
    print(f"# census の全数表 {len(rows)} 行のうち、特許許諾の範囲が作品を超える (S2 / S3): {len(beyond)} 本")
    print()
    unconditional = []
    for lid in beyond:
        p = CACHE / f"{lid}.txt"
        if not p.exists():
            print(f"## {lid}: 原文がキャッシュに無い")
            continue
        t = " ".join(p.read_text(encoding="utf-8", errors="replace").split())
        c = next((m for m in (rx.search(t) for rx in COND) if m), None)
        e = TERM.search(t)
        print(f"## {lid}")
        print(f"- 条件: {('> ' + c.group(0)) if c else '（見つからない）'}")
        print(f"- 終了: {('> ' + e.group(0)) if e else '（見つからない）'}")
        if not c:
            unconditional.append(lid)
    print()
    print(f"# 作品を超える特許許諾 ∧ 条件が見つからない: {len(unconditional)} 本 {unconditional}")
    print("# (0 本なら §1.133 の主張を再現する。分類 S1 / S2 / S3 は census の読みに依拠し、この道具は検証しない)")
    return 0


if __name__ == "__main__":
    if sys.version_info < (3, 10):
        sys.exit("python 3.10+ が要る")
    sys.exit(main())
