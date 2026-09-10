#!/usr/bin/env python3
"""measure_gap_claim.py — ACD-1.0 が主張する gap を、承認済みライセンス全数に対して測る。

**なぜ在るか**: `LICENSES/ACD-1.0.submission.md` §B.0 は審査者に対して
*"That claim is measurable, and I measured it … The command is in the repository."* と述べる。
**その約束は、実際に走るものが在って初めて真である** —— 2026-09-10 に §B.0 を測定へ書き換えた
その日、**約束だけが先に入った**ので同じ増分で追加した（#122 / #123 と同じ族: **検証可能ですらない
約束を入口や送信面に置かない**）。

**測っているもの**: SPDX License List の `isOsiApproved` な全ライセンス本文に、
ACD-1.0 §6 / §8.4 / §9 が扱う主題の語が現れるか。

**測っていないもの（重要）**: **効果**。permissive ライセンスは「すべての利用」を許すことで
機械学習を暗黙に許している。**語の不在は効果の不在ではない。**
この script が示せるのは「**明示的に扱っている承認済みライセンスは無い**」までである。

使い方:
    python3 .github/scripts/measure_gap_claim.py            # 要約だけ
    python3 .github/scripts/measure_gap_claim.py --verbose  # 該当 licenseId も出す

ネットワークが要る（SPDX の公開 JSON を取得する）。CI では走らせない
—— **外部サービスへの定期取得は壊れやすい**（`CLAUDE.md` §7 の方針）。
"""
from __future__ import annotations

import json
import re
import sys
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
INDEX = "https://spdx.org/licenses/licenses.json"
DETAIL = "https://spdx.org/licenses/{}.json"

# 主題ごとの検索語。**正規表現ではなく素の部分文字列**にしてある ——
# 検出器が凝るほど、外れたときに気付きにくい（2026-09-10 に折り返しヘッダで実証）。
TERMS = {
    "machine learning": "§6 (ML を明示的に扱うか)",
    "text and data mining": "§6 (TDM を明示的に扱うか)",
    "data mining": "§6 (TDM の別表記)",
    "machine-generated": "§9 (機械生成物を扱うか)",
    "machine generated": "§9 (別表記)",
    "subsist": "§9 (権利が生じているかの語彙)",
}


def _get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")


def main() -> int:
    verbose = "--verbose" in sys.argv
    index = json.loads(_get(INDEX))
    osi = [l["licenseId"] for l in index["licenses"] if l.get("isOsiApproved")]
    print(f"SPDX License List {index.get('licenseListVersion')} — OSI-approved: {len(osi)}")

    hits: dict[str, list[str]] = {t: [] for t in TERMS}
    near_patent_output: list[str] = []
    failures: list[str] = []
    for lid in osi:
        try:
            text = (json.loads(_get(DETAIL.format(lid))).get("licenseText") or "").lower()
        except Exception:            # noqa: BLE001 — 取得失敗は「未測定」として数える
            failures.append(lid)
            continue
        for term in TERMS:
            if term in text:
                hits[term].append(lid)
        # §8.4 の枝: 特許の近傍に output が現れるか (250 字窓)
        for m in re.finditer(r"\boutputs?\b", text):
            if "patent" in text[max(0, m.start() - 250):m.start() + 250]:
                near_patent_output.append(lid)
                break

    for term, why in TERMS.items():
        found = hits[term]
        print(f"  {term:22} {len(found):3d}  {why}" + (f"  {found}" if verbose and found else ""))
    print(f"  {'output near patent':22} {len(near_patent_output):3d}  §8.4 (特許がモデル/出力に及ぶか)"
          + (f"  {near_patent_output}" if verbose and near_patent_output else ""))
    if failures:
        print(f"  ⚠ 取得失敗 {len(failures)} 件 —— **失敗は 0 件として数えない**: {failures}")

    print("\n**この出力が establish しないこと**: 機械学習が許諾されていないこと。"
          "permissive ライセンスは「すべての利用」を許すことで暗黙に許している。"
          "**語の不在は効果の不在ではない。**")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
