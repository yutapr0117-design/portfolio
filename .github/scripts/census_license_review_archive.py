#!/usr/bin/env python3
"""census_license_review_archive.py — `license-review` の**全期間**から、提出の分布を数える道具

**なぜ在るか。** ドシエが持っていた提出の統計は、**33 か月**（決議）と **44 か月**（スレッド）の
窓で測ったものだった。**`license-review` のアーカイブは 2007-12 から在る。**
**#87 の規律** —— *「名称検索は下限であって全数調査ではない」* —— **を、窓の側にも当てる。**

**この道具が答える 2 つの問い。**

1. **提出はどれくらい engagement を得るのか**（返信ゼロの基準率・通数の中央値）。
   **我々の沈黙を読むには、率ではなく基準率が要る**（`against.md` #109）。
2. **我々の類型（公有化の献呈 / PD 等価）は、19 年で何回出たのか。**
   **#84（なぜもう一つ）と B2（採用 1 件）が依拠している参照クラスそのものである。**

**⚠ これは `license-review` の数である。** 我々の 2026-08-26 の投稿は **`license-discuss`** に
在るので、**この基準率を我々の沈黙に直接当ててはならない。** 別のリストの別の母集団である。

**CI には入れない（意図的）。** 199 か月分の取得が要る。
`verify_dossier_quotations.py` / `measure_list_verbosity.py` と同じく手で回す道具。

使い方:
    python3 .github/scripts/census_license_review_archive.py --fetch    # 199 か月を取得して数える
環境変数 `ARCHIVE_CACHE`（既定 /tmp/arcfull）に月次 mbox を置く。**保存先は `rounds/` ではない**
（`rounds/` は「何と言われたか / 何と言ったか」の記録であって、読んだものの置き場ではない）。
"""
import argparse
import collections
import os
import quopri
import re
import statistics
import sys
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
BASE = "https://lists.opensource.org/pipermail/license-review_lists.opensource.org/"
CACHE = os.environ.get("ARCHIVE_CACHE", "/tmp/arcfull")

# 件名が**承認依頼の形で始まる**ものだけを提出と数える。**メタ議論を落とすため** ——
# 緩い判定（件名のどこかに "submission" 等）は "recent submissions merit no action" のような
# 議論スレッドを拾い、返信ゼロ率を 16.5% へ押し上げる（実測）。厳しい判定では 10.1%。
STRICT = re.compile(
    r"^(for approval|request for approval|request for legacy approval|submission of"
    r"|submitting|official submission|approval request|license submission|for approval of)\b", re.I)
# 我々の類型。**名称で数えるのは下限**なので、件名に出ない提出は取りこぼす（#87）。
PD = re.compile(r"public.?domain|dedication|unlicense|CC0|0BSD|WTFPL|waiver|no.?rights", re.I)


def months():
    idx = urllib.request.urlopen(
        urllib.request.Request(BASE, headers={"User-Agent": UA}), timeout=60
    ).read().decode("utf-8", "replace")
    # index は `.txt.gz` へリンクしている。**`.txt` で探すと 0 件になる**（初版で実際にそうなった）。
    return sorted(set(re.findall(r'href="(\d{4}-[A-Z][a-z]+)\.txt\.gz"', idx)))


def load(ms, fetch):
    os.makedirs(CACHE, exist_ok=True)
    rows = []
    for m in ms:
        path = os.path.join(CACHE, m + ".txt")
        if not os.path.exists(path):
            if not fetch:
                continue
            try:
                d = urllib.request.urlopen(
                    urllib.request.Request(BASE + m + ".txt", headers={"User-Agent": UA}),
                    timeout=90).read().decode("utf-8", "replace")
                open(path, "w", encoding="utf-8").write(d)
            except Exception as exc:  # noqa: BLE001
                print("FETCH FAILED", m, exc, file=sys.stderr)
                continue
        blob = open(path, encoding="utf-8", errors="replace").read()
        for msg in re.split(r"\nFrom ", blob):
            s = re.search(r"^Subject: ([^\n]+(?:\n[ \t][^\n]+)*)", msg, re.M)
            if s:
                rows.append((m, " ".join(s.group(1).split())))
    return rows


def decode_words(s):
    """件名の encoded-word を復号する。

    **これを忘れると、同じスレッドが複数に割れる。** 2026-09-15 の初版はこれを欠いており、
    `license-discuss` では PUWL への返信が別スレッドへ落ちて「返信ゼロ」に見え、
    `license-review` では提出スレッドが 105 → 99 に、返信ゼロが 12 → 10 に見えた。
    **どちらも結論は変えなかったが、数は変えた。**
    """
    def _q(m):
        try:
            return quopri.decodestring(m.group(1).replace("_", " ")).decode("utf-8", "replace")
        except Exception:  # noqa: BLE001
            return m.group(1)

    def _b(m):
        try:
            return base64.b64decode(m.group(1) + "===").decode("utf-8", "replace")
        except Exception:  # noqa: BLE001
            return m.group(1)

    s = re.sub(r"=\?[^?]+\?[qQ]\?([^?]*)\?=", _q, s)
    return re.sub(r"=\?[^?]+\?[bB]\?([^?]*)\?=", _b, s)


def norm(s):
    s = decode_words(s)
    s = re.sub(r"^(Re:|Fwd:|\[License-review\]|\[EXTERNAL\]|\s)+", "", s, flags=re.I)
    return " ".join(s.replace("[License-review]", "").replace("[EXTERNAL]", "").split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    args = ap.parse_args()
    ms = months()
    rows = load(ms, args.fetch)
    if not rows:
        print("no messages — run with --fetch", file=sys.stderr)
        return 1
    th = collections.Counter()
    first = {}
    for mon, subj in rows:
        k = norm(subj)
        th[k] += 1
        first.setdefault(k, mon)
    span = sorted({m for m, _ in rows}, key=lambda x: (int(x.split("-")[0]), x))
    print(f"span {span[0]} → {span[-1]}   months {len(span)}   messages {len(rows)}   threads {len(th)}")

    sub = [(k, th[k], first[k]) for k in th if STRICT.match(k)]
    zero = [s for s in sub if s[1] == 1]
    counts = [s[1] for s in sub]
    print(f"\n提出スレッド {len(sub)}   返信ゼロ {len(zero)} ({100*len(zero)/len(sub):.1f}%)"
          f"   中央値 {statistics.median(counts):.0f} 通   最大 {max(counts)}")
    print("  ⚠ これは license-review の数である。我々の 2026-08-26 の投稿は license-discuss に在る。")

    pd = [s for s in th.items() if PD.search(s[0])]
    print(f"\n我々の類型に見えるスレッド（名称一致・**下限**）: {len(pd)}")
    for k, v in sorted(pd, key=lambda x: first[x[0]]):
        print(f"  {first[k]:16} {v:4} 通  {k[:88]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
