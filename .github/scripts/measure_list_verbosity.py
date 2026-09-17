#!/usr/bin/env python3
"""measure_list_verbosity.py — 我々のメールの長さと密度を、同じ窓の他の参加者と比べる道具

**なぜ在るか。** 2026-09-15、OSI の moderator が steward へ直接こう求めた ——
*"Map out the **length and density** of your emails and compare it with the length and density of
other emails sent to these two mailing lists by humans."*（`rounds/2026-09-15-offlist-…txt`）。

**この問いは測れる。** 測れる問いに散文で答えるのは、`REVIEWERS.md` が掲げる *check us* に反する。
**だから道具を置いて、誰でも同じ数を出せるようにした。**

**2 つの長さを分けて数えるのが要点である。**
  * **delivered** = **アーカイブに展開されて出る量**（本文 + 添付 + 引用）。
    **アーカイブを読む人が出会うのはこちらである。**
  * **inbox**     = **読み手の画面に出る本文だけ**（`next part` より前）。
    **⚠ 2026-09-17 訂正**: 初版はこの区別が無く、`delivered` を「inbox に届いた本文全体」と
    呼んでいた。**添付は本文ではない。**
  * **prose**     = その人が新しく書いた散文だけ（引用行・署名・フッタ・MIME の次パートを除く）。
    **「長い文章を書く人か」を見るのはこちらである。**
**片方だけで語ると、有利にも不利にも見せられる** —— 2026-08-26 の ACD 投稿は
**アーカイブ上 5,778 語 / 本文 867 語 / prose 867 語**である ——
**条文は本文に貼られたのではなく添付されていた**（本文自身が *"attached as ACD-1.0.txt"* と述べる）。
**どれも真だが答える問いが違う。**

密度の代理指標は **1 文あたりの語数**と **1 段落あたりの語数**。**短い文・短い段落は
読みやすさの側**なので、「長い」と「密である」は別に測る。

**CI には入れない（意図的）。** 公開アーカイブの取得が要る。
`verify_dossier_quotations.py` / `measure_clause_clarity.py` と同じく、手で回す道具である。

使い方:
    python3 .github/scripts/measure_list_verbosity.py --fetch       # 既定の 3 か月を取得して測る
    python3 .github/scripts/measure_list_verbosity.py --months 2026-June,2026-July
環境変数 `LIST_CACHE`（既定 /tmp/arc2）にアーカイブを置く。
"""
import argparse
import collections
import glob
import os
import re
import statistics
import sys
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
CACHE = os.environ.get("LIST_CACHE", "/tmp/arc2")
LISTS = ("license-review", "license-discuss")
DEFAULT_MONTHS = ("2026-July", "2026-August", "2026-September")
URL = "https://lists.opensource.org/pipermail/{}_lists.opensource.org/{}.txt"
# steward の From 行。pipermail は日本語表示名を RFC 2047 で符号化するので両方を見る。
OURS = re.compile(r"yuta\.yokoi|5qiq5Lq")


def fetch(months):
    os.makedirs(CACHE, exist_ok=True)
    for lst in LISTS:
        for mon in months:
            path = os.path.join(CACHE, f"{lst}-{mon}.txt")
            if os.path.exists(path):
                continue
            req = urllib.request.Request(URL.format(lst, mon), headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                open(path, "w", encoding="utf-8").write(r.read().decode("utf-8", "replace"))
            print("fetched", lst, mon, file=sys.stderr)


def split_parts(msg):
    """**3 つに分ける** —— body（読み手の画面に出る本文）/ attached（添付として届いたもの）/
    prose（その人が新しく書いた散文）。

    **⚠ 2026-09-17 の訂正。** 初版は `delivered` を「受け手の inbox に届いた本文全体」と
    呼び、**pipermail が `next part` の後ろへ展開した添付まで本文として数えていた。**
    実測すると 2026-08-26 の ACD 投稿は **本文 867 語 + 添付（ACD-1.0.txt）**で、
    アーカイブの 5,778 語は**アーカイブの見え方**であって受信箱の見え方ではない
    （本文自身が *"The complete license text is attached as ACD-1.0.txt."* と述べている）。
    **「届いた」と「アーカイブに出ている」を同じ語で呼んだのが誤り**で、その語を根拠に
    「8 月の投稿は長すぎた」と読んでいた。**添付は注意を要求する形が本文とは違う。**

    `delivered` は body+attached の合計として残す（アーカイブを読む人が出会う量であり、
    それも真の問いに答える）が、**どちらの数かを呼び分ける。**
    """
    body = msg.split("\n\n", 1)[1] if "\n\n" in msg else ""
    delivered = len(body.split())
    cut = body.find("-------------- next part")
    head = body[:cut] if cut > 0 else body
    kept = []
    for line in head.split("\n"):
        s = line.rstrip()
        if s.startswith(">"):
            continue
        if s.startswith("-- ") or s.startswith("_______"):
            break
        if s.strip().startswith("----- "):
            break
        if re.match(r"^On .{5,80}wrote:$", s.strip()):
            continue
        if "The opinions expressed in this email" in s:
            break
        kept.append(s)
    inbox = len(head.split())          # 読み手の画面に出る本文だけ
    attached = delivered - inbox       # pipermail が展開した添付・スクラブ告知
    return delivered, "\n".join(kept).strip(), inbox, attached


def measure(months):
    rows = []
    for lst in LISTS:
        for mon in months:
            path = os.path.join(CACHE, f"{lst}-{mon}.txt")
            if not os.path.exists(path):
                continue
            blob = open(path, encoding="utf-8", errors="replace").read()
            for msg in [("From " + m) for m in re.split(r"\nFrom ", blob)]:
                frm = re.search(r"^From: ([^\n]+)", msg, re.M)
                if not frm:
                    continue
                delivered, prose, inbox, attached = split_parts(msg)
                if len(prose.split()) < 5 and delivered < 20:
                    continue
                sents = [x for x in re.split(r"(?<=[.!?])\s+", prose) if len(x.split()) > 2]
                paras = [p for p in re.split(r"\n\s*\n", prose) if p.strip()]
                words = len(prose.split())
                rows.append(dict(
                    list=lst, frm=frm.group(1), delivered=delivered, inbox=inbox,
                    attached=attached, prose=words,
                    date=(re.search(r"^Date: ([^\n]+)", msg, re.M).group(1)
                          if re.search(r"^Date: ([^\n]+)", msg, re.M) else ""),
                    wps=(words / len(sents) if sents else 0),
                    wpp=(words / len(paras) if paras else 0),
                    ours=bool(OURS.search(frm.group(1)))))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--months", default=",".join(DEFAULT_MONTHS))
    args = ap.parse_args()
    months = tuple(m.strip() for m in args.months.split(",") if m.strip())
    if args.fetch:
        fetch(months)
    rows = measure(months)
    if not rows:
        print("no messages measured — run with --fetch", file=sys.stderr)
        return 1
    ours = [r for r in rows if r["ours"]]
    oth = [r for r in rows if not r["ours"]]
    med = lambda pop, k: statistics.median([r[k] for r in pop])
    pct = lambda v, k: 100 * sum(1 for x in sorted(r[k] for r in oth) if x < v) / len(oth)
    print(f"window: {', '.join(months)}   messages: {len(rows)} "
          f"(ours {len(ours)} / others {len(oth)})\n")
    print(f"{'':24}{'delivered':>12}{'prose':>10}{'words/sentence':>16}{'words/para':>12}")
    for label, pop in (("OURS   median", ours), ("OTHERS median", oth)):
        print(f"{label:24}{med(pop,'delivered'):>12.0f}{med(pop,'prose'):>10.0f}"
              f"{med(pop,'wps'):>16.1f}{med(pop,'wpp'):>12.1f}")
    print()
    print("our messages (percentile is against the other participants):")
    for r in sorted(ours, key=lambda x: -x["delivered"]):
        print(f"  {r['date'][:17]:19}{r['list']:17}"
              f"delivered={r['delivered']:5} ({pct(r['delivered'],'delivered'):4.1f}th)  "
              f"prose={r['prose']:5} ({pct(r['prose'],'prose'):4.1f}th)")
    tot = collections.Counter()
    cnt = collections.Counter()
    for r in rows:
        key = "OURS" if r["ours"] else re.sub(r"\s*\(.*", "", r["frm"])
        tot[key] += r["prose"]
        cnt[key] += 1
    rank = sorted(tot.items(), key=lambda x: -x[1])
    ourrank = [i for i, (k, _) in enumerate(rank, 1) if k == "OURS"]
    print(f"\ntotal prose words per participant — our rank: "
          f"{ourrank[0] if ourrank else 'n/a'} of {len(rank)}   "
          f"share of all prose words: {100*tot['OURS']/sum(tot.values()):.1f}%   "
          f"share of all messages: {100*cnt['OURS']/sum(cnt.values()):.1f}%")
    for i, (k, v) in enumerate(rank[:8], 1):
        print(f"  {i:>2} {k[:34]:36}{cnt[k]:>4} msgs{v:>8} words")
    return 0


if __name__ == "__main__":
    sys.exit(main())
