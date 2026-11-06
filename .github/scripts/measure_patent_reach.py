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
    python3 .github/scripts/measure_patent_reach.py --express # 明示の特許許諾を持つ全本の条件の文

**`--express` (2026-11-04)**: 主張は「範囲 ∧ 無条件 ∧ 終了なし」の連言なので、明示の特許許諾を持つ本が
すべて条件を持つなら、範囲の分類 (S1 / S2 / S3 = 読みの判定) に依拠せずに同じ結論が出る。全本の条件の文を
逐語で出し、見つからない本を数える。census の「明示」列には依拠する (明示か否かは patent の語の有無で確かめられる)。
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CACHE = Path(os.environ.get("GAP_CENSUS_CACHE", "/tmp/gap-census-cache"))
CENSUS = Path(os.environ.get("GAP_CENSUS_FILE", ROOT / "LICENSES" / "ACD-1.0.gap-census.md"))

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


# 義務の形の語を優先し、TERMS AND CONDITIONS のような見出しに一致しないよう素の conditions は置かない。
EXPRESS_COND = [re.compile(p + r"[^.]{0,150}", re.I) for p in (
    r"must (?:ensure|be included|retain|include|reproduce|be accompanied|cause|give|make|provide|keep|duplicate|inform)",
    r"(?:subject to|under) the following conditions?",
    r"provided that",
    r"on condition that",
    r"shall (?:retain|include|reproduce|provide|cause|ensure|give|keep|duplicate|inform|distribute|make available)",
    r"you (?:must|shall|agree to|may not)",
    r"(?:is|are) required to",
    r"\bmust\b",
)]


def verify_sources(meta: dict, rows: list[str]) -> bool:
    """全数が揃っていなければ結論を出さない。

    2026-11-06 まで、原文が欠けた本は黙って飛ばされ、最後の "0" は欠けたまま完全に見えた (別の AI の patch の
    指摘・オーナーが渡した)。census の sha256 も照合するので、census と取得物が別の時点のものなら止まる。
    """
    cells = [[c.strip().strip("`") for c in ln.split("|")] for ln in rows]
    ids = [c[1] for c in cells]
    digests = meta.get("sha256")
    issues = []
    if not ids or len(set(ids)) != len(ids):
        issues.append("the census is empty or has duplicate identifiers")
    if meta.get("approved_nondeprecated") != len(ids):
        issues.append("the census row count differs from the fetched SPDX population")
    if meta.get("failed") or meta.get("fetched") != len(ids):
        issues.append("the SPDX fetch was incomplete")
    if not isinstance(digests, dict):
        issues.append("the source checksum manifest is missing")
        digests = {}
    if set(digests) != set(ids):
        issues.append("the census identifiers and the source checksum manifest differ")
    for c in cells:
        lid, recorded = c[1], c[2]
        source = CACHE / f"{lid}.txt"
        if not source.is_file():
            issues.append(f"{lid}: the SPDX source is missing")
            continue
        actual = hashlib.sha256(source.read_bytes()).hexdigest()
        if lid in digests and actual != digests[lid]:
            issues.append(f"{lid}: the SPDX source differs from the fetched checksum")
        if actual[:12] != recorded:
            issues.append(f"{lid}: the census was generated from a different text")
    if issues:
        for issue in issues[:20]:
            print(f"ERROR: the comparison is incomplete: {issue}", file=sys.stderr)
        print(f"ERROR: {len(issues)} problem(s). No full-population result is given. If the SPDX list has moved since the "
              "census was made, run: python3 .github/scripts/generate_gap_census.py", file=sys.stderr)
        return False
    return True


def express(rows: list[str]) -> int:
    ids = []
    for ln in rows:
        cells = [c.strip() for c in ln.split("|")]
        if len(cells) > 4 and cells[4].startswith("明示"):
            ids.append(cells[1].strip("`"))
    missing = []
    for lid in sorted(ids):
        t = " ".join((CACHE / f"{lid}.txt").read_text(encoding="utf-8", errors="replace").split())
        m = next((m for m in (rx.search(t) for rx in EXPRESS_COND) if m), None)
        print(f"{lid}: {m.group(0) if m else '(none found)'}")
        if not m:
            missing.append(lid)
    print(f"\n# Of {len(ids)} licences with an express patent grant, no obligation sentence found in: {len(missing)} {missing}")
    if missing:
        print("# REVIEW REQUIRED: the conjunction in gap-measurements.md §1.133 is not reproduced. "
              "Read the full text of each licence listed above before relying on it.")
        return 1
    print("# This reproduces the conjunction in gap-measurements.md §1.133 without relying on the scope classification. "
          "Whether each sentence found is a condition is for a person to read.")
    return 0


# 出力は英語で書く (2026-11-06)。これは審査者が自分で走らせる道具で、提出の最も強い主張を再現する。
# 終了コードは 0 = 主張を再現した / 1 = 反例が出た / 2 = 全数が揃わず結論を出していない。
def main() -> int:
    if not (CACHE / "_meta.json").exists():
        print(f"SPDX sources not found in {CACHE}. Run first: python3 .github/scripts/generate_gap_census.py --fetch")
        return 2
    meta = json.loads((CACHE / "_meta.json").read_text(encoding="utf-8"))
    rows = [ln for ln in CENSUS.read_text(encoding="utf-8").splitlines() if ln.startswith("| `")]
    if not verify_sources(meta, rows):
        return 2
    if "--express" in sys.argv:
        return express(rows)
    beyond = []
    for ln in rows:
        cells = [c.strip() for c in ln.split("|")]
        if len(cells) > 5 and cells[5] in ("S2", "S3"):
            beyond.append(cells[1].strip("`"))
    print(f"# SPDX licenseListVersion {meta.get('licenseListVersion')} / releaseDate {meta.get('releaseDate')} / "
          f"fetched {meta.get('fetched_at')} / OSI-approved and not deprecated: {meta.get('approved_nondeprecated')}")
    print(f"# Of {len(rows)} rows in the census, the patent grant reaches beyond the work (S2 / S3) in: {len(beyond)}")
    print()
    unconditional = []
    for lid in beyond:
        p = CACHE / f"{lid}.txt"
        t = " ".join(p.read_text(encoding="utf-8", errors="replace").split())
        c = next((m for m in (rx.search(t) for rx in COND) if m), None)
        e = TERM.search(t)
        print(f"## {lid}")
        print(f"- condition: {('> ' + c.group(0)) if c else '(none found)'}")
        print(f"- termination: {('> ' + e.group(0)) if e else '(none found)'}")
        if not c:
            unconditional.append(lid)
    print()
    print(f"# Patent grant reaching beyond the work with no condition found: {len(unconditional)} {unconditional}")
    if unconditional:
        print("# REVIEW REQUIRED: the claim in gap-measurements.md §1.133 is not reproduced. "
              "Read the full text of each licence listed above before relying on it.")
        return 1
    print("# This reproduces the claim in gap-measurements.md §1.133. The S1 / S2 / S3 classification is a reading "
          "recorded in the census; this tool does not verify it.")
    return 0


if __name__ == "__main__":
    if sys.version_info < (3, 10):
        sys.exit("Python 3.10 or later is required")
    sys.exit(main())
