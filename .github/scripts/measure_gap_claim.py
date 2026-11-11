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

**向き（2026-11-11・portfolio-aa の依頼）**: §2.4 / §4.4（許諾を互いに頼らせない）と §2.5（信頼を目的と
述べ、約因の欠けで無効を主張しない）の語は、承認済みの本文にも現れるが**逆の向きで**現れる ——
*estoppel* は「黙示の許諾を生まない」の列挙に、*consideration* は「条件の対価」に。語の有無を数えると
「在る」と出て誤る。ゆえに文ごとに向きを機械で仕分けて出す。**仕分けは候補であって判定ではない**
（--verbose で文を出すので、人が読む）。

使い方:
    python3 .github/scripts/measure_gap_claim.py                 # SPDX の承認済み全件（ネットワーク）
    python3 .github/scripts/measure_gap_claim.py --verbose       # 該当 licenseId と向きごとの文も出す
    python3 .github/scripts/measure_gap_claim.py --texts DIR     # DIR/<licenseId>.txt を読む（census の cache と同じ形）
    python3 .github/scripts/measure_gap_claim.py --wp-json F...  # opensource.org の WP API の license ページ（content.rendered）
        取得元: WP_LICENSE_API の page=1, 2, … を順に取って保存したもの（この道具は取得しない）。
        出力に各 file の sha256 の先頭を出すので、取得の記録（日付と sha256）と結べる
    python3 .github/scripts/measure_gap_claim.py --self-test     # 向きの仕分けを固定の文で確かめる（ネットワーク不要）

既定はネットワークが要る（SPDX の公開 JSON を取得する）。CI では走らせない
—— **外部サービスへの定期取得は壊れやすい**（`CLAUDE.md` §7 の方針）。
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
INDEX = "https://spdx.org/licenses/licenses.json"
# --wp-json の入力の取得元 (2026-10-17 の取得もこの形・portfolio-aa の依頼で明記した)。1 ページ 100 件
WP_LICENSE_API = "https://opensource.org/wp-json/wp/v2/license?orderby=modified&order=desc&per_page=100&page={}"
DETAIL = "https://spdx.org/licenses/{}.json"

# 出力は英語で書く (2026-11-06)。§B.0 が審査者に走らせる道具で、結果が読めなければ約束が果たせない。
# 主題ごとの検索語。**正規表現ではなく素の部分文字列**にしてある ——
# 検出器が凝るほど、外れたときに気付きにくい（2026-09-10 に折り返しヘッダで実証）。
TERMS = {
    "machine learning": "§6 (names machine learning)",
    "text and data mining": "§6 (names text and data mining)",
    "data mining": "§6 (the same, other wording)",
    "machine-generated": "§9 (names machine-generated material)",
    "machine generated": "§9 (the same, other wording)",
    "subsist": "§9 (the vocabulary of whether a right subsists)",
}

# 向きつきの語族: (表示名, 文を拾う正規表現, ACD の条, [(向きの名, その向きと読む正規表現)])。
#   向きは上から順に当て、どれにも当たらない文は "other"。ACD の向きの名は "ACD's direction" で始める。
DIRECTED = [
    ("independent(ly) of", r"\bindependent(?:ly)? of\b", "§2.4 / §4.4", [
        ("ACD's direction: a grant stands independently of another",
         r"\b(?:grant\w*|licen[cs]e\w*|permission\w*|covenant\w*|waiver\w*|dedication|sections? \d)")]),
    ("fallback", r"\bfall-?back\b", "§2.4 / §4.4", [
        ("ACD's direction: one grant is not a fallback for another", r"\b(?:not|none|no)\b[^.;]{0,40}\bfall-?back\b")]),
    ("estoppel / estopped", r"\bestop(?:pel|ped)\b", "§2.5", [
        ("ACD's direction: binds the grantor not to deny the grant", r"\bestopped\b|\bwill not assert\b"),
        ("denies an implied licence (no rights by implication, estoppel or otherwise)",
         r"\bno (?:rights?|licen[cs]es?)\b|\bexcept as expressly\b|\bimplication,? (?:or )?estoppel\b")]),
    ("consideration", r"\bconsideration\b", "§2.5", [
        ("ACD's direction: the grant is not to fail for want of consideration",
         r"\b(?:want|lack|absence|failure) of consideration\b|\bwithout consideration\b"),
        ("the price of a condition (in consideration of, and as a condition to, the licences)",
         r"\bin consideration of,? and as (?:an? )?(?:express )?condition\b")]),
    ("rely / reliance", r"\brel(?:y|ies|ied|ying|iance)\b", "§2.5", [
        ("ACD's direction: reliance is stated as the instrument's purpose", r"\b(?:intend\w*|purpose)\b"),
        ("disclaims reliance", r"\bdisclaim\w*\s+(?:any\s+)?reliance\b")]),
]


def sentences(text: str) -> list[str]:
    return re.split(r"(?<=[.;])\s+", " ".join(text.split()))


def directions(text: str) -> dict[str, dict[str, list[str]]]:
    """{語族: {向き: [文]}}。語族の語を持つ文ごとに、最初に当たった向きへ入れる。"""
    out: dict[str, dict[str, list[str]]] = {}
    for name, rx, _cl, dirs in DIRECTED:
        for s in sentences(text):
            if re.search(rx, s, re.I):
                label = next((d for d, drx in dirs if re.search(drx, s, re.I)), "other")
                out.setdefault(name, {}).setdefault(label, []).append(s)
    return out


# 自己試験の文: 承認済みの本文 (EPL-2.0 / APSL-2.0 / GPL-2.0 / LGPL-2.1) と ACD-1.4 草案から逐語で取った。
#   仕分けの正規表現を変えたら、ここが同じ向きに落ちることを --self-test で確かめる
_SELF_TEST = [
    ("Except as expressly stated in Sections 2(a) and 2(b) above, Recipient receives no rights or licenses to the "
     "intellectual property of any Contributor under this Agreement, whether expressly, by implication, estoppel or "
     "otherwise.", "estoppel / estopped", "denies an implied licence"),
    ("In consideration of, and as a condition to, the licenses granted to You under this License, You hereby grant to "
     "any person or entity receiving or distributing Covered Code under this License a non-exclusive, royalty-free, "
     "perpetual, irrevocable license.", "consideration", "the price of a condition"),
    ("The act of running the Program is not restricted, and the output from the Program is covered only if its contents "
     "constitute a work based on the Program (independent of having been made by running the Program).",
     "independent(ly) of", "other"),
    ("Many people have made generous contributions to the wide range of software distributed through that system in "
     "reliance on consistent application of that system;", "rely / reliance", "other"),
    ("4.4 The licence in Section 4.1 is granted independently of Section 3, and not as a fallback for it: it takes "
     "effect whether or not Section 3 does.", "independent(ly) of", "ACD's direction"),
    ("4.4 The licence in Section 4.1 is granted independently of Section 3, and not as a fallback for it: it takes "
     "effect whether or not Section 3 does.", "fallback", "ACD's direction"),
    ("The Dedicator will not assert that this Dedication is revocable or ineffective for want of consideration or "
     "formality, and is estopped from doing so to the extent the law of any jurisdiction gives that principle effect.",
     "consideration", "ACD's direction"),
    ("The Dedicator will not assert that this Dedication is revocable or ineffective for want of consideration or "
     "formality, and is estopped from doing so to the extent the law of any jurisdiction gives that principle effect.",
     "estoppel / estopped", "ACD's direction"),
    ("that reliance is the purpose of this Dedication and not merely a foreseeable consequence of it.",
     "rely / reliance", "ACD's direction"),
]


def self_test() -> int:
    bad = []
    for text, family, want in _SELF_TEST:
        got = list(directions(text).get(family, {"(no sentence)": []}))
        if len(got) != 1 or not got[0].startswith(want):
            bad.append(f"{family}: expected '{want}…', got {got} for {text[:60]!r}")
    for b in bad:
        print("FAIL:", b)
    print(f"self-test: {len(_SELF_TEST) - len(bad)} / {len(_SELF_TEST)} sentences sorted as expected")
    return 1 if bad else 0


def _get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")


def _corpus(argv: list[str]):
    """(母集団の説明, [(id, 本文 or None)])。None は取得の失敗 (0 として数えない)。"""
    if "--texts" in argv:
        d = Path(argv[argv.index("--texts") + 1])
        files = sorted(d.glob("*.txt"))
        return f"{len(files)} text file(s) in {d}", [(f.stem, f.read_text(encoding="utf-8", errors="replace")) for f in files]
    if "--wp-json" in argv:
        pages, digests = [], []
        for f in argv[argv.index("--wp-json") + 1:]:
            if f.startswith("--"):
                break
            raw = Path(f).read_bytes()
            digests.append(f"{Path(f).name} sha256 {hashlib.sha256(raw).hexdigest()[:12]}")
            pages += json.loads(raw.decode("utf-8"))
        rows = [(p.get("slug", "?"), html.unescape(re.sub(r"<[^>]+>", " ", (p.get("content") or {}).get("rendered", ""))))
                for p in pages]
        return (f"opensource.org WP API license pages: {len(rows)} ({'; '.join(digests)})\n"
                f"  source: {WP_LICENSE_API.format('1, 2, …')}"), rows

    index = json.loads(_get(INDEX))
    osi = [l["licenseId"] for l in index["licenses"] if l.get("isOsiApproved")]
    rows = []
    for lid in osi:
        try:
            rows.append((lid, json.loads(_get(DETAIL.format(lid))).get("licenseText") or ""))
        except Exception:            # noqa: BLE001 — 取得失敗は「未測定」として数える
            rows.append((lid, None))
    return f"SPDX License List {index.get('licenseListVersion')} — OSI-approved: {len(osi)}", rows


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()
    verbose = "--verbose" in sys.argv
    label, rows = _corpus(sys.argv)
    print(label)

    hits: dict[str, list[str]] = {t: [] for t in TERMS}
    near_patent_output: list[str] = []
    failures: list[str] = []
    directed: dict[str, dict[str, list[tuple[str, str]]]] = {}
    for lid, raw in rows:
        if raw is None:
            failures.append(lid)
            continue
        text = raw.lower()
        for fam, by in directions(raw).items():
            for d, ss in by.items():
                directed.setdefault(fam, {}).setdefault(d, []).append((lid, ss[0]))
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
    print(f"  {'output near patent':22} {len(near_patent_output):3d}  §8.4 (a patent grant reaching models or outputs)"
          + (f"  {near_patent_output}" if verbose and near_patent_output else ""))
    print("\nWords that approved texts also use, sorted by direction (machine-sorted candidates; read the sentences with --verbose):")
    for fam, _rx, clause, dirs in DIRECTED:
        by = directed.get(fam, {})
        ids = {lid for v in by.values() for lid, _s in v}
        print(f"  {fam:22} {len(ids):3d}  {clause}")
        for d in [d for d, _ in dirs] + ["other"]:
            v = by.get(d, [])
            print(f"      {len({lid for lid, _s in v}):3d}  {d}" + (f"  {sorted({lid for lid, _s in v})}" if verbose and v else ""))
            if verbose:
                for lid, sent in v:
                    print(f"           {lid}: {sent[:200]}")
    if failures:
        print(f"  WARNING: {len(failures)} fetch failure(s). A failure is not counted as zero: {failures}")

    print("\nWhat this output does not establish: that machine learning is not permitted. A permissive licence "
          "permits it implicitly by permitting every use. The absence of a word is not the absence of an effect.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
