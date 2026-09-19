#!/usr/bin/env python3
"""verify_dossier_quotations.py — ドシエの逐語引用が、実在の source に在るかを確かめる道具

**なぜ在るか。** ドシエは外部の人物・ページに帰属させた英語の逐語引用を大量に含む。
**引用が現物と違う提出は、審査者が最初に気づく種類の誤りである**し、
本リポジトリの規律は *「我々の読みは誤りうるが、何と言われたかの記録は誤ってはならない」* と述べている。
**その規律を、宣言ではなく実測で確かめるための道具。**

**CI には入れない（意図的）。** 検証には公開アーカイブの取得が要り、
CLAUDE.md §7 が *「自動監視は CI に入れない（外部フォーラムの定期取得は壊れやすい）」* と定めている。
**これは手で回す道具であって Check ではない。** 結果は `LICENSES/AUDIT-LEDGER.md` へ記録する。

使い方:
    # ⚠ **cache を指定せずに回すと、ほぼ何も照合できない。** 既定は空の /tmp/arc で、
    # 2026-09-19 の実測では **322 件中 100 件しか確認できず、残り 222 件が「未確認」**になった
    # ——**道具は動いているのに、入力が空である**（`against.md` #165）。
    DOSSIER_ARCHIVE_CACHE=<取得済みアーカイブのディレクトリ> \
        python3 .github/scripts/verify_dossier_quotations.py
    # 不足月を自分で取りに行く（同じ cache へ書く）:
    DOSSIER_ARCHIVE_CACHE=<同上> python3 .github/scripts/verify_dossier_quotations.py --fetch
    # 未確認を全件出す（既定は上位 15 件）:
    DOSSIER_ALL=1 DOSSIER_ARCHIVE_CACHE=<同上> python3 ...

**corpus の置き場所の規約**: 月次アーカイブは `<cache>/*.txt` であれば名前は問わない
（`discuss-2024-10.txt` でも `license-discuss-2024-October.txt` でもよい）。
**2026-09-19 時点で必要な範囲は 2012 / 2017〜2026 の両リスト**で、
**2017 / 2018 / 2021 / 2022 は「ドシエが引いているのに一度も取得していなかった」**
——取得後に確認数が 238 → 249 へ動いた。**「未確認」が減らないときは、まず月の欠落を疑う。**

**⚠ 検出器を信じる前に、検出器を疑うこと。** 2026-09-14 の初版は
「引用らしき文字列」を 4,976 件と数え、そのほとんどが **markdown の太字記法**だった。
規約 (`*"..."*`) に絞って 495、人名の近傍に絞って 251 まで落ちた。
**母数が大きすぎるときは、母数の作り方が間違っている。**
"""
import argparse
import collections
import glob
import json
import os
import re
import sys
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
CACHE = os.environ.get("DOSSIER_ARCHIVE_CACHE", "/tmp/arc")
# 帰属を示す手掛かり。**名前で絞るのは下限であって全数調査ではない** (#87) が、
# 「外部に帰属させた引用」を取り出す目的にはこれで足りる。
NAME = re.compile(r"(Smith|Chestek|Fontana|Villa|Landley|Piana|Berkus|Perens|Sado|Dolan"
                  r"|Duan|Atkinson|Vidal|Maffulli|Anna|McCoy|Mehl|Webber|Woolley|氏)")


def norm(text):
    """比較用の正規化。**アーカイブは清書テキストではない**ことを前提に畳む。

    **空白**: 行またぎで折り返された引用を「不一致」と誤報告した実例が 2026-09-09 にある。
    **quoted-printable**: pipermail は `=\n` の軟改行と `=E2=80=99` 形式の escape を含む。
    **約物**: 丸い引用符・ダッシュ・省略記号が、我々の側と source 側で食い違う。

    **2026-09-14 の実測**: 空白だけを畳む版で 156/251、ここまで畳んで **193/257**。
    **37 件は「引用が違う」のではなく「読み方が硬すぎた」だけだった。**
    """
    text = text.replace("=\n", "")
    text = re.sub(r"=[0-9A-F]{2}", " ", text)
    return " ".join(re.sub(r"[^A-Za-z0-9]+", " ", text.lower()).split())


def load_sources(root="."):
    """照合先: rounds/ の一次資料 + 本文 + 取得済みアーカイブ。"""
    out = []
    pats = [f"{root}/LICENSES/rounds/*", f"{CACHE}/*.txt",
            f"{root}/LICENSES/ACD-1.0.txt", f"{root}/LICENSES/ACD-1.1.txt", f"{root}/LICENSE"]
    for pat in pats:
        for f in glob.glob(pat):
            try:
                out.append(norm(open(f, encoding="utf-8", errors="replace").read()))
            except OSError:
                continue
    return " || ".join(out)


def collect_quotes(root="."):
    """`*"..."*` 形式で、人名の近傍にある英語の逐語引用を集める。"""
    quotes = {}
    for path in sorted(glob.glob(f"{root}/LICENSES/*.md")):
        lines = open(path, encoding="utf-8").read().split("\n")
        for n, line in enumerate(lines):
            context = " ".join(lines[max(0, n - 3):n + 3])
            if not NAME.search(context):
                continue
            for m in re.finditer(r'\*"([^"]{25,400})"\*', line):
                # **生のまま集める。** norm() は約物を落とすので、ここで正規化すると
                # **省略記号が消え、present() の分割照合が永久に発火しなくなる**
                # （2026-09-14 に実際にそうなり、確認数が 193 → 155 へ落ちた）。
                q = re.sub(r"[*`]", "", " ".join(m.group(1).split()))
                if len(q.split()) < 5:
                    continue
                if sum(ord(c) < 128 for c in q) / len(q) <= 0.9:
                    continue
                quotes.setdefault(q, set()).add(f"{os.path.basename(path)}:{n + 1}")
    return quotes


def present(quote, blob):
    """引用が source に在るか。**正規化は比較の時にだけ行う。**

    **省略記号を挟む部分引用は断片ごとに照合する** —— そのために、分割は
    *生の引用*に対して行い、正規化はそのあとで各断片に当てる。
    """
    if norm(quote) in blob:
        return True
    segs = [norm(s) for s in re.split(r"\.{3}|…", quote)]
    segs = [s for s in segs if len(s.split()) >= 5]
    return bool(segs) and all(s in blob for s in segs)


def needed_months(missing, root="."):
    """未確認の引用の近傍にある日付から、取得すべき月を導出する。"""
    need = collections.Counter()
    for locs in missing.values():
        for loc in locs:
            fname, _, ln = loc.partition(":")
            try:
                lines = open(f"{root}/LICENSES/{fname}", encoding="utf-8").read().split("\n")
            except OSError:
                continue
            i = int(ln)
            ctx = " ".join(lines[max(0, i - 4):i + 3])
            for y, mm in re.findall(r"(20\d\d)-(\d\d)", ctx):
                if 1 <= int(mm) <= 12:
                    need[(y, MONTHS[int(mm) - 1])] += 1
    return need


def fetch(months, limit=30):
    os.makedirs(CACHE, exist_ok=True)
    got = 0
    for (y, m), _ in months.most_common(limit):
        for lst in ("license-review", "license-discuss"):
            dest = f"{CACHE}/{lst}-{y}-{m}.txt"
            if os.path.exists(dest):
                continue
            url = (f"https://lists.opensource.org/pipermail/"
                   f"{lst}_lists.opensource.org/{y}-{m}.txt")
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                open(dest, "wb").write(urllib.request.urlopen(req, timeout=60).read())
                got += 1
            except Exception:      # noqa: BLE001 — 存在しない月は普通に起きる
                continue
    return got


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true", help="不足月をアーカイブから取得する")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()

    quotes = collect_quotes(args.root)
    blob = load_sources(args.root)
    miss = {q: sorted(v) for q, v in quotes.items() if not present(q, blob)}
    print(f"帰属つき英語の逐語引用: {len(quotes)}")
    print(f"  確認できた: {len(quotes) - len(miss)}   確認できない: {len(miss)}")

    if args.fetch and miss:
        n = fetch(needed_months(miss, args.root))
        print(f"  アーカイブを {n} file 取得して再照合")
        blob = load_sources(args.root)
        miss = {q: v for q, v in miss.items() if not present(q, blob)}
        print(f"  再照合後: 確認できた {len(quotes) - len(miss)} / 確認できない {len(miss)}")

    if miss:
        print("\n--- 未確認（全件） ---")
        for q, locs in list(miss.items())[: (999 if os.environ.get("DOSSIER_ALL") else 15)]:
            print(f"  [{locs[0]}] {q[:110]}")
        print("\n**未確認 = 誤引用ではない。** 我々自身の文を強調で括ったものと、"
              "まだ取得していない月の両方が入る。**分類してから結論すること。**")
    return 0


if __name__ == "__main__":
    sys.exit(main())
