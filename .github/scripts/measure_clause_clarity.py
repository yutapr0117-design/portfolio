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
環境変数 `CLARITY_CACHE`（既定 /tmp/lic）に比較対象の本文を置く。
"""
import argparse
import os
import re
import statistics
import sys
import urllib.request

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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true",
                    help="比較対象の本文を SPDX から取得してキャッシュする")
    args = ap.parse_args()
    if args.fetch:
        fetch_peers()
    here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    rows = []
    for name, path in [("ACD-1.0", "LICENSES/ACD-1.0.txt"),
                       ("ACD-1.1 draft", "LICENSES/ACD-1.1-DRAFT.txt")]:
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
        print(f"\n⚠ 比較対象が手元に無い: {missing} —— `--fetch` を付けて取得せよ。"
              "**欠けたまま出した表を「比較した」と読まないこと。**", file=sys.stderr)


if __name__ == "__main__":
    main()
