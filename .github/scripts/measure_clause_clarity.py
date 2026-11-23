#!/usr/bin/env python3
"""measure_clause_clarity.py — 文の長さと従属の重なりを、**方法を書いたうえで**測る道具

**なぜ在るか。** OSI の承認基準 8 条のうち 7 条は我々の側で確かめられるが、**8 条目（英語と
しての明晰さ）だけが判断の余地を残す**。ドシエはそこへ代理指標（文長・長文率・従属の重なり）
を置いており、**その数字は register の冒頭に出て、B3（長さ）の読みを支えている。**

**問題は数字ではなく、方法が書かれていなかったことだった。** 2026-09-14 の敵対的検証
（主張の種類 6）で `review-corpus.md` §1.70a の表を当たると、**文の切り方は記録されているのに
最後の 2 列（「うち列挙型」「うち従属節 2 つ以上」）の定義がどこにも無かった** ——
**定義の無い数字は再実行できない。**

**そして方法を書いて測り直すと、結論が反転する列があった。** 記録は ACD-1.0 の
「従属節 2 つ以上」を **0.0%** とし、そこから *「解析の負荷という意味では比較した中で最も軽い」*
と結論していた。本 script の定義（下記）では **61.1%** で、比較群の中でも高い側に来る。
**どちらが正しいかは決められない ——記録された方法が無いからである。**
**決められるのは「この結論は、方法を書いた指標では支持されない」ということだけ。**

**CI には入れない（意図的）。** 比較対象の本文取得に外部 fetch が要る。
`verify_dossier_quotations.py` と同じ扱いで、**手で回す道具であって Check ではない。**

定義（**この 3 つが、記録が欠いていたもの**）:
  * 文の切れ目 = `[.;:]` の後に空白を挟んで大文字・引用符・開き括弧・`数字.数字`・`数字. ` が来る位置。
    （条番号が本文と同じ行に続く形式を罰しないため。§1.70a の訂正で確定した条件）
  * 「列挙型」   = 45 語超の文のうち、カンマを 3 つ以上含むもの。
  * 「従属節 2 つ以上」= 45 語超の文のうち、従属節を導く語（which / that / where / when / if /
    because / unless / although / while / whether / who / whom / whose / provided that /
    to the extent that）が **2 回以上**現れるもの。
    **⚠ これは「入れ子」ではなく「2 回以上の出現」である。** 並列する 2 つの関係節も数える。
    **記録の 0.0% が「入れ子だけを数えた」結果である可能性は排除できない** ——
    だから本 script は記録を「誤り」とは言わず、**別の定義での値**を出す。

使い方:
    python3 .github/scripts/measure_clause_clarity.py                # 手元のキャッシュで測る
    python3 .github/scripts/measure_clause_clarity.py --fetch        # 比較対象を SPDX から取得
    python3 .github/scripts/measure_clause_clarity.py --diff         # 作業中の草案と直前の確定版の差だけ (外部 fetch なし)

**--diff (2026-11-23・5e の依頼)**: 次版の方針「各変更は語数と 45 語超の割合の差を申告する」(1.5 の (B)) のために、
作業中の草案と直前の確定版の本文 (条項部分) を同じ定義で測り、語数・文数・45 語超の割合の差と、45 語超の文のうち
片側にだけ在るもの (新しく長くなった文・長くなくなった文) を出す。ACD 同士だけなので外部 fetch は要らない。
環境変数 `CLARITY_CACHE`（既定 /tmp/lic）に比較対象の本文を置く。
"""
import argparse
import os
import pathlib
import re
import statistics
import sys
import urllib.request

from measure_quote_drift import _current_draft_version

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
CACHE = os.environ.get("CLARITY_CACHE", "/tmp/lic")
PEERS = ["Apache-2.0", "MPL-2.0", "EPL-2.0", "OSL-3.0", "CDDL-1.0"]
SPDX = "https://spdx.org/licenses/{}.json"

SPLIT = re.compile(r'(?<=[.;:])\s+(?=[A-Z"(]|\d+\.\d|\d+\. )')
SUB = re.compile(r"\b(which|that|where|when|if|because|unless|although|while|whether"
                 r"|who|whom|whose|provided that|to the extent that)\b", re.I)


def sentences(text):
    """段落を保ったまま折り返しを解き、文へ割る。"""
    text = text.replace("\r", "")
    text = re.sub(r"\n{2,}", "\x00", text)
    text = text.replace("\n", " ").replace("\x00", "\n\n")
    out = []
    for para in text.split("\n\n"):
        para = re.sub(r"\s+", " ", para).strip()
        if para:
            out += [s.strip() for s in SPLIT.split(para) if len(s.strip().split()) > 2]
    return out


def row(name, text):
    ss = sentences(text)
    wl = [len(s.split()) for s in ss]
    lg = [s for s in ss if len(s.split()) > 45]
    enum = [s for s in lg if s.count(",") >= 3]
    two = [s for s in lg if len(SUB.findall(s)) >= 2]
    pct = lambda n: round(100 * n / len(lg), 1) if lg else 0.0
    return (name, len(ss), round(statistics.mean(wl), 1), statistics.median(wl), max(wl),
            round(100 * len(lg) / len(ss), 1), pct(len(enum)), pct(len(two)))


def body(text, start="1. DEFINITIONS", end="END OF TERMS"):
    """ACD の本文（条項部分）だけを取る。前文と末尾の注記は条文ではない。"""
    if start in text and end in text:
        return text[text.index(start):text.index(end)]
    return text


def fetch_peers():
    os.makedirs(CACHE, exist_ok=True)
    import json
    for lid in PEERS:
        path = os.path.join(CACHE, lid + ".txt")
        if os.path.exists(path):
            continue
        req = urllib.request.Request(SPDX.format(lid), headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(data.get("licenseText", ""))
        print("fetched", lid, file=sys.stderr)


def diff(here):
    """作業中の草案と直前の確定版の差 (--diff)。返り値は表示した行の数 (テスト用)。"""
    _v = _current_draft_version()
    major, minor = _v.split(".")
    prev = f"{major}.{int(minor) - 1}"
    texts = {}
    for name, path in ((f"ACD-{prev}", f"LICENSES/ACD-{prev}.txt"), (f"ACD-{_v} draft", f"LICENSES/ACD-{_v}-DRAFT.txt")):
        with open(os.path.join(here, path), encoding="utf-8") as fh:
            texts[name] = body(fh.read())
    (a_name, a), (b_name, b) = texts.items()
    ra, rb = row(a_name, a), row(b_name, b)
    wa, wb = len(a.split()), len(b.split())
    print("words = 条項部分 (1. DEFINITIONS 〜 END OF TERMS) の語数。草案冒頭の申告 (題名から) とは範囲が違う")
    print(f"{'':16}{'words':>7}{'sents':>7}{'mean':>7}{'45+%':>7}{'sub2%':>7}")
    for r, w in ((ra, wa), (rb, wb)):
        print(f"{r[0]:16}{w:>7}{r[1]:>7}{r[2]:>7}{r[5]:>7}{r[7]:>7}")
    print(f"{'diff':16}{wb - wa:>+7}{rb[1] - ra[1]:>+7}{round(rb[2] - ra[2], 1):>+7}{round(rb[5] - ra[5], 1):>+7}{round(rb[7] - ra[7], 1):>+7}")
    long_a = {s for s in sentences(a) if len(s.split()) > 45}
    long_b = {s for s in sentences(b) if len(s.split()) > 45}
    shown = 3
    for label, only in (("45 語超になった文 (草案にだけ在る)", long_b - long_a), ("45 語超でなくなった文 (確定版にだけ在る)", long_a - long_b)):
        print(f"\n{label}: {len(only)}")
        for s in sorted(only, key=lambda x: -len(x.split())):
            print(f"  [{len(s.split())}] {' '.join(s.split()[:14])} …")
            shown += 1
    return shown


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true",
                    help="比較対象の本文を SPDX から取得してキャッシュする")
    ap.add_argument("--diff", action="store_true",
                    help="作業中の草案と直前の確定版の差だけを出す (外部 fetch なし)")
    args = ap.parse_args()
    if args.diff:
        diff(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        return
    if args.fetch:
        fetch_peers()
    here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    rows = []
    # 投稿した 1.0、最新の凍結版、作業中の草案を測る。出す版は申請の日に確定する最新版なので、版を決め打ちすると
    # 確定した日に出す版の行が消える (2026-11-07: 1.1 を名指していたので、1.4 確定後の表に 1.4 が出なかった)。
    _v = _current_draft_version()
    _fixed = sorted((p.name[4:-4] for p in pathlib.Path(here, "LICENSES").glob("ACD-[0-9].[0-9]*.txt")
                     if not p.name.endswith("-DRAFT.txt")), key=lambda v: tuple(map(int, v.split("."))))
    for name, path in [(f"ACD-{v}", f"LICENSES/ACD-{v}.txt") for v in dict.fromkeys((_fixed[0], _fixed[-1]))] + [
            (f"ACD-{_v} draft", f"LICENSES/ACD-{_v}-DRAFT.txt")]:
        with open(os.path.join(here, path), encoding="utf-8") as fh:
            rows.append(row(name, body(fh.read())))
    missing = []
    for lid in PEERS:
        path = os.path.join(CACHE, lid + ".txt")
        if not os.path.exists(path):
            missing.append(lid)
            continue
        with open(path, encoding="utf-8") as fh:
            rows.append(row(lid, fh.read()))
    hdr = ("licence", "sents", "mean", "median", "max", "45+%", "enum%", "sub2%")
    print(f"{hdr[0]:16}{hdr[1]:>6}{hdr[2]:>7}{hdr[3]:>8}{hdr[4]:>6}{hdr[5]:>7}{hdr[6]:>7}{hdr[7]:>7}")
    for r in rows:
        print(f"{r[0]:16}{r[1]:>6}{r[2]:>7}{r[3]:>8}{r[4]:>6}{r[5]:>7}{r[6]:>7}{r[7]:>7}")
    if missing:
        print(f"\nWARNING: comparison texts are not available: {missing}. Run with --fetch. "
              "A table with texts missing is not a comparison.", file=sys.stderr)


if __name__ == "__main__":
    main()
