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
    # 人名の近傍に限らず、斜体の引用をすべて当てる (語を動かした引用は人名の無い行にもある):
    DOSSIER_ALL=1 DOSSIER_ARCHIVE_CACHE=<同上> python3 .github/scripts/verify_dossier_quotations.py --all-italics
    # 入口の面の引用を全 corpus に当てて manifest を更新する (Check 472n が読む):
    DOSSIER_ARCHIVE_CACHE=<同上> python3 .github/scripts/verify_dossier_quotations.py --record-entry
    # rounds の各通がアーカイブに逐語で在るか (切った通は、切った位置の直後のアーカイブを出す):
    DOSSIER_ARCHIVE_CACHE=<同上> python3 .github/scripts/verify_dossier_quotations.py --rounds [LICENSES/rounds/<file> ...]
    # 逐語を含む通の差出人と年が、ドシエの同じ文の人名 (X 氏) と年に合うか (帰属の取り違えを拾う・人が読んで決める):
    DOSSIER_ARCHIVE_CACHE=<同上> python3 .github/scripts/verify_dossier_quotations.py --attribution
    # 「要約」と書いた語句が、実は原文に逐語で在るか (在れば、引用の記法と出典を付けるべき):
    DOSSIER_ARCHIVE_CACHE=<同上> python3 .github/scripts/verify_dossier_quotations.py --summaries
    # OSI のサイトの取得物も照合先にする:
    DOSSIER_EXTRA_SOURCES=~/osi-fetch/fetch DOSSIER_ARCHIVE_CACHE=<同上> python3 ...

**cache は古くなる。** 2026-11-07 に cache が 9 月までで、10-14 の発言 2 件が未確認に落ちた。月の途中で取った
file と、最新の file より後の終わった月は、実行の冒頭に警告で出る。

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
import calendar
import collections
import datetime
import glob
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
CACHE = os.environ.get("DOSSIER_ARCHIVE_CACHE", "/tmp/arc")
ENTRY_MANIFEST = ".github/scripts/entry_quotes_verified.txt"
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
    # **pipermail の HTML→text 変換は、リンクされた語の直後に `<http://...>` を挿入する。**
    # 実例 (2026-09-27 実測): *"the text currently served from the ids.nus.edu.sg URL"* は
    # source 側で `ids.nus.edu.sg\n<http://ids.nus.edu.sg> URL` になっており、**語の並びが
    # 割られて一致しない**。落とすのは `<scheme://…>` の形だけにする ——素の URL まで消すと、
    # **URL そのものについての引用**（"the URL was as the specification says" 等）を照合できなくなる。
    text = re.sub(r"<[a-z][a-z0-9+.-]*://[^>]*>", " ", text)
    return " ".join(re.sub(r"[^A-Za-z0-9]+", " ", text.lower()).split())


_ITALIC_PLAIN = re.compile(r'\*"([^"\n]+)"\*')
# 内側の引用符を対で許す形。*"... the "covered work" is?"* のような引用は、内側の " で切れて
# 照合から黙って漏れていた (portfolio-00 の指摘・2026-11-08: LICENSES/*.md の英語の引用 32 件)。
_ITALIC_INNER = re.compile(r'\*"((?:[^"\n]|(?<=\s)"[^"\n*]{1,80}"(?=[\s.,;:!?)\'’]))+?)"\*')


def italic_quotes(line, minlen=12, maxlen=100000):
    """行の斜体の引用 *"..."* を返す。内側の引用符を含む形も拾う (両方の正規表現の和)。"""
    out = []
    for rx in (_ITALIC_PLAIN, _ITALIC_INNER):
        for q in rx.findall(line):
            if minlen <= len(q) <= maxlen and q not in out:
                out.append(q)
    return out


def load_sources(root=".", cache=True):
    """照合先: rounds/ の一次資料 + 本文 + 取得済みアーカイブ。cache=False は CI が持つ分だけを読む。"""
    out = []
    # **2026-11-01 是正 (portfolio-bb の報告から)**: (a) 本文は 1.0 / 1.1 だけを読んでいたので、
    #   1.2 以降の凍結版と現行草案の逐語引用が「未確認」に数えられていた —— 版は glob で導出する。
    #   (b) rounds/ の長い一次資料は行境界で `-NofM` に分割して保存してあり (Check 365 の 1,000 行
    #   上限のため)、**分割の境目をまたぐ引用は、どの断片にも丸ごとは無い**。断片を番号順に
    #   連結してから読む (無改変保存の規約は bytes の分割であって、連結すれば原文に戻る)。
    # OSI のサイトやイベント頁の取得物はアーカイブに無い。DOSSIER_EXTRA_SOURCES (":" 区切りの dir) で足す。
    #   タグを落として読むので、JSON と HTML の両方で語の並びが残る。
    for _dir in filter(None, os.environ.get("DOSSIER_EXTRA_SOURCES", "").split(":") if cache else []):
        for _dp, _dn, _fn in os.walk(_dir):
            for _f in _fn:
                if _f != "MANIFEST.md":
                    with open(os.path.join(_dp, _f), encoding="utf-8", errors="replace") as _h:
                        out.append(norm(html.unescape(re.sub(r"<[^>]+>", " ", _h.read().replace("\\u2019", "'")))))
    pats = ([f"{CACHE}/*.txt"] if cache else []) + [f"{root}/LICENSES/ACD-*.txt", f"{root}/LICENSE"]
    for pat in pats:
        for f in sorted(glob.glob(pat)):
            try:
                out.append(norm(open(f, encoding="utf-8", errors="replace").read()))
            except OSError:
                continue
    _parts = {}
    for f in sorted(glob.glob(f"{root}/LICENSES/rounds/*")):
        _m = re.match(r"(.*)-(\d+)of(\d+)(\.[^.]+)$", f)
        _key, _idx = ((_m.group(1) + _m.group(4)), int(_m.group(2))) if _m else (f, 0)
        _parts.setdefault(_key, []).append((_idx, f))
    for _key, _fs in sorted(_parts.items()):
        _txt = ""
        for _, f in sorted(_fs):
            try:
                _txt += open(f, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
        out.append(norm(_txt))
    return " || ".join(out)


def load_self(root="."):
    """**自分自身の成果物**（ドシエ本体・commit message・README 等）を、外部 source とは
    **別の blob** として読む。

    **なぜ分けるか。** ドシエは `*"..."*` を「逐語引用」の記法として使い、その対象は
    *人の発言*とは限らない ——**自分の commit message・自分の節の注記・自分の README の
    呼び出し文**も同じ記法で引く。**人名の近傍にある**という抽出条件だけでは両者を分けられず、
    その結果「未確認」の大半が**外部照合の対象ですらないもの**で埋まり、
    **残差の数が判断に使えなくなる**（2026-09-19 に 73 件中の大半がこれだった・`against.md` #165）。

    **⚠ この blob を外部照合に混ぜてはならない。** 混ぜると、**人の発言を誤って書き写しても
    自分の file と一致して「確認できた」になる** ——道具が守ろうとしている当のものが壊れる。
    だから `present()` には渡さず、**外部で確認できなかったものだけ**をここへ当てる。
    """
    # **⚠ 引用記法そのものを落としてから読む。** 落とさないと **引用は自分が書かれている file に
    # 必ず在る**ので、この分類は **全件を自己引用と判定する**（2026-09-19 に実際にそうなった
    # ——324 件中 73 件の残差が「自己引用 73 / 出典に当たれていない 0」という、
    # **一見きれいで中身の無い数**を返した）。**判定したいのは「同じ語が、引用符の外の、
    # 我々自身の地の文に在るか」**である。
    strip = re.compile(r'\*"[^"]{1,400}"\*')
    out = []
    for pat in (f"{root}/LICENSES/*.md", f"{root}/README.md",
                f"{root}/docs/architecture/*.md"):
        for f in glob.glob(pat):
            try:
                out.append(norm(strip.sub(" ", open(f, encoding="utf-8", errors="replace").read())))
            except OSError:
                continue
    try:
        out.append(norm(subprocess.run(["git", "log", "--format=%B", "-n", "400"],
                                       cwd=root, capture_output=True, text=True).stdout))
    except Exception:          # noqa: BLE001 — git が無い環境でも道具は動くべき
        pass
    return " || ".join(out)


def collect_quotes(root=".", named=True):
    """`*"..."*` 形式の英語の逐語引用を集める。named は人名の近傍のものに絞る。"""
    quotes = {}
    for path in sorted(glob.glob(f"{root}/LICENSES/*.md")):
        lines = open(path, encoding="utf-8").read().split("\n")
        for n, line in enumerate(lines):
            context = " ".join(lines[max(0, n - 3):n + 3])
            if named and not NAME.search(context):
                continue
            for _raw in italic_quotes(line, 25, 400):
                # **生のまま集める。** norm() は約物を落とすので、ここで正規化すると
                # **省略記号が消え、present() の分割照合が永久に発火しなくなる**
                # （2026-09-14 に実際にそうなり、確認数が 193 → 155 へ落ちた）。
                q = re.sub(r"[*`]", "", " ".join(_raw.split()))
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
    # **角括弧は 2 通りに読める。** `[sic]` と `code[s]` は**挿入なので落とす**のが正しく、
    # `appropri[ate]` は**補完なので中身を残す**のが正しい。**どちらが正しいかは書き手の意図で、
    # 記法からは決まらない**ので、**両方を試して片方でも一致すれば可**とする
    # （2026-09-19: `[sic]` を付けて出典へ戻した引用が、その `[sic]` のせいで
    # 「出典に当たれていない」に落ちた ——**忠実さを上げた修正が、忠実さの検査を落とした**）。
    import re as _re
    for _v in (_re.sub(r"\s*\[[^\]]*\]", "", quote), _re.sub(r"[\[\]]", "", quote), quote):
        if norm(_v) in blob:
            return True
        _s = [norm(x) for x in _re.split(r"\.{3}|…", _v)]
        _k = [x for x in _s if len(x.split()) >= 3] or [x for x in _s if len(x.split()) >= 2]
        if _k and all(x in blob for x in _k):
            return True
    if norm(quote) in blob:
        return True
    segs = [norm(s) for s in re.split(r"\.{3}|…", quote)]
    # **短い断片を捨てない。** 5 語未満を捨てる実装では、断片が全部短い引用
    # （*"3888 words … excessively wordy and proscriptive"* ——2 語と 4 語）で
    # **segs が空になり、照合せずに「未確認」を返していた**（2026-09-19 実測）。
    # **短い断片も要求するのは緩和ではなく強化である**（満たすべき条件が増える）。
    keep = [s for s in segs if len(s.split()) >= 3]
    if not keep:
        keep = [s for s in segs if len(s.split()) >= 2]
    return bool(keep) and all(s in blob for s in keep)


def needed_months(missing, root="."):
    """未確認の引用の近傍にある日付から、取得すべき月を導出する。

    **近傍は「前後数行」ではなく「その引用が属する節」である。** 2026-09-20 に、
    正しく逐語である引用が 2 件「未確認」として残った ——Pamela Chestek 氏の
    2024-03-14（日付は 20 行上の表に在る）と Simon Phipps 氏の 2018-10
    （日付は 30 行上の節見出しに在る）。**どちらもアーカイブに実在し、逐語でも一致した。**
    窓が 4 行だったので、道具は「取りに行くべき月」を導出できず、
    **結果は「誤引用かもしれない」と読める形で出ていた。**
    ——**検出器が 0 を返したら、まず当て方を疑う。**
    """
    need = collections.Counter()
    for locs in missing.values():
        for loc in locs:
            fname, _, ln = loc.partition(":")
            try:
                lines = open(f"{root}/LICENSES/{fname}", encoding="utf-8").read().split("\n")
            except OSError:
                continue
            i = int(ln)
            # 直上の見出しまで遡る（節の中の日付は、その節の引用すべてに効く）。
            start = 0
            for j in range(min(i, len(lines)) - 1, -1, -1):
                if lines[j].startswith("#"):
                    start = j
                    break
            ctx = " ".join(lines[start:i + 3])
            for y, mm in re.findall(r"(20\d\d)-(\d\d)", ctx):
                if 1 <= int(mm) <= 12:
                    need[(y, MONTHS[int(mm) - 1])] += 1
    return need


def needed_years(missing, root="."):
    """年しか書かれていない引用のために、その年の全月を候補にする。

    **月が導出できないのは引用の欠陥ではなく、我々の書き方の性質である。**
    節に `YYYY` しか無ければ、その年の 12 か月を候補に入れる。
    """
    need = collections.Counter()
    for locs in missing.values():
        for loc in locs:
            fname, _, ln = loc.partition(":")
            try:
                lines = open(f"{root}/LICENSES/{fname}", encoding="utf-8").read().split("\n")
            except OSError:
                continue
            i = int(ln)
            start = 0
            for j in range(min(i, len(lines)) - 1, -1, -1):
                if lines[j].startswith("#"):
                    start = j
                    break
            ctx = " ".join(lines[start:i + 3])
            for y in set(re.findall(r"\b(20[12]\d)\b", ctx)):
                for m in MONTHS:
                    need[(y, m)] += 1
    return need


def fetch(months, limit=200):
    """**上限は「取りに行かなかった月」を作る。** 既定が 30 だった間、導出された月の裾は
    静かに落ち、その月から引いた引用は「未確認」として残った ——
    **未取得と誤引用が同じ欄に出る。** 月の総数は導出結果で頭打ちになるので、
    実質的に全件を取りに行く値にしてある。"""
    os.makedirs(CACHE, exist_ok=True)
    got = 0
    for (y, m), _ in months.most_common(limit):
        for lst in ("license-review", "license-discuss"):
            dest = f"{CACHE}/{lst}-{y}-{m}.txt"
            # [FIX 2026-10-10] 0 バイトの file は「取得済み」ではない。旧実装は open() を urlopen()
            # より先に呼んでいたため、存在しない月（未来の月・投稿の無い月）で空 file が残り、
            # 以後その月は二度と取りに行かれなかった —— 後から投稿が載っても照合に入らない。
            if os.path.exists(dest) and os.path.getsize(dest) > 0:
                continue
            url = (f"https://lists.opensource.org/pipermail/"
                   f"{lst}_lists.opensource.org/{y}-{m}.txt")
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                data = urllib.request.urlopen(req, timeout=60).read()   # 取得に成功してから書く
                open(dest, "wb").write(data)
                got += 1
            except Exception:      # noqa: BLE001 — 存在しない月は普通に起きる
                continue
    return got


def stale_months():
    """cache の欠けを返す: その月が終わる前に取得した file と、最新の file より後の終わった月。"""
    months = {m: i for i, m in enumerate(calendar.month_name) if m}
    today = datetime.date.today()
    partial, newest = [], {}
    for path in glob.glob(f"{CACHE}/*.txt"):
        m = re.search(r"([a-z-]+?)[-_](\d{4})-([A-Z][a-z]+)\.txt$", os.path.basename(path))
        if m and m.group(3) in months:
            year, month = int(m.group(2)), months[m.group(3)]
            end = datetime.date(year + month // 12, month % 12 + 1, 1)
            if datetime.date.fromtimestamp(os.path.getmtime(path)) < end <= today:
                partial.append(os.path.basename(path))
            newest[m.group(1)] = max(newest.get(m.group(1), (0, 0)), (year, month))
    behind = [f"{lst} は {y}-{mo:02d} まで" for lst, (y, mo) in sorted(newest.items())
              if (y, mo) < ((today.year, today.month - 1) if today.month > 1 else (today.year - 1, 12))]
    return sorted(partial) + behind


def entry_quotes(root="."):
    """審査者と採用者が最初に読む面の斜体の引用を {引用: 最初の場所} で返す。話者名の条件は付けない。"""
    from measure_citation_drift import FACES, FIRST_READ

    found = {}
    # register の英語の索引も、入口と同じく審査者が英語で最初に読む面 (portfolio-00 の提案・2026-11-08)
    faces = [f for f in FACES if FIRST_READ.search(f)] + ["ACD-OSI-BOTTLENECKS.md"]
    for face in faces:
        with open(f"{root}/LICENSES/{face}", encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                for raw in italic_quotes(line, 12):
                    q = re.sub(r"[*`]", "", raw)
                    if len(q.split()) >= 3 and not re.search(r"[ぁ-んァ-ヶ一-龠]", q):
                        found.setdefault(q, f"{face}:{n}")
    return found


def entry_key(quote):
    return hashlib.sha256(norm(quote).encode("utf-8")).hexdigest()[:16]


def read_entry_manifest(root="."):
    """確認済みの引用の hash と、我々自身の文 (`own: `) の集合を返す。"""
    keys, own = set(), set()
    with open(f"{root}/{ENTRY_MANIFEST}", encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("own: "):
                own.add(norm(line[5:]))
            elif line.strip() and not line.startswith("#"):
                keys.add(line.strip())
    return keys, own


def record_entry(root="."):
    """入口の引用を全 corpus に当て、確認できたものの hash を manifest へ書く。`own: ` の行は手で足して残す。"""
    blob = load_sources(root)
    _, own = read_entry_manifest(root)
    with open(f"{root}/{ENTRY_MANIFEST}", encoding="utf-8") as fh:
        head = [ln for ln in fh if ln.startswith(("#", "own: "))]
    quotes = entry_quotes(root)
    # CI の手元 (rounds/・本文・LICENSE) で確かめられる引用は hash に残さない (2026-11-12): 残すと、草案が後でその句を
    #   失っても hash が引用を解決し続け、Check 472n は緑のままだった (T54 で §8.4 の文を外した日に、外向きの面の引用の
    #   依拠を手で数えた)。そういう引用は Check 472n が毎回本文に当てる。hash はアーカイブでしか確かめられない引用だけ
    base = load_sources(root, cache=False)
    good = sorted({entry_key(q) for q in quotes if norm(q) not in own and present(q, blob) and not present(q, base)})
    bad = {q: [loc] for q, loc in quotes.items() if norm(q) not in own and not present(q, blob)}
    print(f"入口の引用 {len(quotes)} 件: アーカイブで確認 {len(good)} / 本文・rounds で確認 (hash に残さない) "
          f"{sum(1 for q in quotes if norm(q) not in own and present(q, base))} / 我々の文 {len(own)} / 確認できない {len(bad)}")
    for q, locs in bad.items():
        print(f"  [{locs[0]}] {q[:110]}")
    for score, loc, seg in near_misses(bad, blob):
        print(f"  前後が一致 {score:.2f} [{loc}] {seg[:100]}")
    # 確認できない引用があるときは書かない。corpus が足りないと確認済みが消える (2026-11-07 に変数なしで 60 件消えた)。
    if bad:
        print("manifest は書き換えていない。原文に当てるか、cache と DOSSIER_EXTRA_SOURCES を足して回し直す")
        return 1
    with open(f"{root}/{ENTRY_MANIFEST}", "w", encoding="utf-8") as fh:
        fh.write("".join(head) + "\n".join(good) + "\n")
    return 0


def near_misses(miss, blob):
    """未確認のうち、断片の先頭か末尾の 5 語以上が原文に在るものを返す。

    **語を落とした引用は全文では一致しないが、前後は一致する。** 話者名で分類する規則は、知らない名前の
    近くの誤りを見落とす (2026-11-07: Engelfriet 氏の *also when saying* を *even when saying* にしていた)。
    自分の文の強調もここに残るので、結果は 1 件ずつ読む。
    """
    out = []
    for q, locs in miss.items():
        best = None
        for seg in re.split(r"\.{3}|…", q):
            words = norm(seg).split()
            if len(words) < 6 or " ".join(words) in blob:
                continue
            if " ".join(words[:5]) not in blob and " ".join(words[-5:]) not in blob:
                continue
            head = next((k for k in range(len(words) - 1, 4, -1) if " ".join(words[:k]) in blob), 0)
            tail = next((k for k in range(len(words) - 1, 4, -1) if " ".join(words[-k:]) in blob), 0)
            if (head or tail) and (best is None or (head + tail) / len(words) > best[0]):
                best = ((head + tail) / len(words), locs[0], seg.strip())
        if best:
            out.append(best)
    return sorted(out, key=lambda x: -x[0])


SUMMARY_LABEL = re.compile(
    r"\*\*([^*]{8,240})\*\*\s*[（(]\s*(?:a summary, not a quotation|a summary|summary|要約)[^)）]*[)）]",
    re.I)


def summaries(root="."):
    """「要約」と書いた語句を原文に当てる (portfolio-00 の提案・2026-11-08)。

    objection-map に「要約」と書いた行が、実は逐語だった (Fontana 氏の 1 行・#2618 で直した)。
    斜体の引用の照合は記法で引用を探すので、要約と名乗った語句は照合の外にある。要約の記法は
    `**語句** (a summary, not a quotation)` と `**語句**（要約）`。一致すれば「要約ではなく引用」で、
    逐語の記法と出典を付けるべき行である。一致しないことは要約であることの証明ではない。
    """
    blob = load_sources(root)
    found = []
    for path in sorted(glob.glob(os.path.join(root, "LICENSES", "*.md"))):
        for i, line in enumerate(open(path, encoding="utf-8").read().splitlines(), 1):
            for m in SUMMARY_LABEL.finditer(line):
                found.append((f"{os.path.basename(path)}:{i}", m.group(1).strip(), present(m.group(1).strip(), blob)))
    verbatim = [f for f in found if f[2]]
    print(f"要約と書いた語句: {len(found)}   うち原文に逐語で在るもの: {len(verbatim)}")
    for loc, phrase, hit in found:
        print(f"  {'逐語 (要約ではない)' if hit else '要約として整合'}  [{loc}] {phrase[:90]}")
    return 0


def rounds(root=".", files=()):
    """`LICENSES/rounds/` の各通が、アーカイブの写しに逐語で在るかを当てる (2026-11-11)。

    rounds は「無改変」を約束する (`rounds/README.md` 規則 1)。引用の始まりで切った通は、切った位置までが
    アーカイブの連続と一致し、その直後がアーカイブでは引用 (`... wrote:` / `-----Original Message-----`) で
    始まるはずである。通ごとに「全文 / 切った (直後のアーカイブを出す) / 一致しない」を出す。portfolio-00 が
    新しい rounds を足すたびに portfolio-9b が手で当てていた照合を道具にした。私信の stub と、mbox の From 行を
    持たない file (サイトの取得物) は当てない。
    """
    blob = "".join(open(p, encoding="utf-8", errors="replace").read() for p in sorted(glob.glob(os.path.join(CACHE, "*.txt"))))
    if not blob:
        print(f"⚠ cache {CACHE} が空。DOSSIER_ARCHIVE_CACHE を指定する")
        return 2
    targets = list(files) or sorted(glob.glob(os.path.join(root, "LICENSES", "rounds", "*.txt")))
    n = whole = cut = 0
    bad, other = [], []
    for f in targets:
        t = open(f, encoding="utf-8").read()
        if "----- begin verbatim -----" not in t or "THE TEXT HAS BEEN WITHDRAWN" in t:
            continue
        body = t.split("----- begin verbatim -----\n", 1)[-1].split("----- end verbatim -----")[0]
        for m in re.split(r"(?m)^(?=From \S+ at \S+  \w{3} \w{3} )", body):
            if not m.startswith("From "):
                continue
            n += 1
            k, head = m.rstrip("\n"), m.split("\n", 1)[0]
            i = blob.find(k)
            if i < 0:
                lo, hi = 0, len(k)
                while lo < hi:
                    mid = (lo + hi + 1) // 2
                    lo, hi = (mid, hi) if blob.find(k[:mid]) >= 0 else (lo, mid - 1)
                bad.append(f"{os.path.basename(f)}: {head[:60]} —— 先頭 {lo} / {len(k)} 字までしか一致しない。次の字 {k[lo:lo + 40]!r}")
                continue
            nxt = blob[i + len(k):i + len(k) + 300]
            if not nxt.strip() or nxt.lstrip("\n").startswith("From "):
                whole += 1
                continue
            cut += 1
            # 切った位置の直後が引用の始まりか (ヘッダの「引用の始まりで切る」の約束どおりか)。それ以外は人が読む
            # 他言語の書き出しも引用の始まりと読む (2026-11-11・portfolio-00 の報告: Piana 氏の "ha scritto:")
            if re.match(r"\s*(?:On .{0,250}?wrote|[^\n]{0,80}wrote:|-{5} ?Original Message|>|From: |_{5,}\s*\n\s*From:|Quoting "
                        r"|[^\n]{0,80} writes:|[^\n]{0,120}(?:ha scritto|a écrit|schrieb|escribió|escreveu|skrev|kirjoitti"
                        r"|napisał|\u043d\u0430\u043f\u0438\u0441\u0430\u043b|schreef|scrisse|écrivait)\s?:)", nxt, re.S):
                continue
            other.append(f"{os.path.basename(f)}: {head[:60]} → アーカイブの続き {nxt.lstrip()[:45]!r}")
    print(f"rounds の通 {n} 件: 全文 {whole} / 切った {cut}（うち引用の始まりでない位置 {len(other)}）/ 一致しない {len(bad)}")
    for o in other:
        print(f"  引用の始まりでない位置で切った (ヘッダが述べる切り方か読む): {o}")
    for b in bad:
        print(f"  一致しない: {b}")
    return 1 if bad else 0


def attribution(root="."):
    """逐語を含む通の差出人と年を、ドシエの同じ文が帰属させている人名 (「X 氏」) と年に当てる (2026-11-12)。

    存在の照合は「その逐語がどこかに在るか」しか見ない。いちばん傷の深い誤りは「在るが、別の人・別の年の文だった」で
    (§1.141 の 4 月の返信の取り違え)、審査者が 1 件見つけるだけで全体の信用が落ちる (portfolio-00 の優先度)。
    通は引用を除いた本文で探す (返信が引いた他人の文を、返信者の文と取り違えないため)。人名と年は、引用の前の同じ文
    (。・表のセル・ —— ・；で区切る) から取り、年は引用の直後 40 字も見る。誤検出は残るので、一覧は人が読んで決める。
    """
    import email.header
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import census_decision_statements as cds

    def who(raw):
        try:
            return str(email.header.make_header(email.header.decode_header(raw)))
        except Exception:
            return raw
    msgs = [(who(cds.field(h, "From")), cds._when(cds.field(h, "Date")), norm(cds.own_text(b))) for _p, h, b in cds.messages()]
    print(f"通 {len(msgs)} 件 (cache {CACHE})")
    seen, tally, out = set(), collections.Counter(), []
    for f in sorted(glob.glob(f"{root}/LICENSES/*.md")):
        for n, line in enumerate(open(f, encoding="utf-8"), 1):
            for raw in italic_quotes(line, 12):
                q = re.sub(r"[*`]", "", raw)
                if len(q.split()) < 4 or re.search(r"[ぁ-んァ-ヶ一-龠]", q):
                    continue
                i = line.find(raw[:30])
                pre = re.split(r"。|\||——|；", line[:max(i, 0)])[-1]
                names = re.findall(r"([A-Z][a-zA-Z'\-]+) 氏", pre)
                # 年は人名の後ろから引用までの間に在るもの、無ければ引用の直後 30 字 (同じ文の読んだ日などを拾わない)
                _after = pre[[m.end() for m in re.finditer(r"[A-Z][a-zA-Z'\-]+ 氏", pre)][-1]:] if names else ""
                years = (re.findall(r"(?<!\d)((?:199|20[0-2])\d)(?!\d)", _after)
                         or re.findall(r"(?<!\d)((?:199|20[0-2])\d)(?!\d)", line[i + len(raw):i + len(raw) + 30]))
                if not names or (names[-1], norm(q)) in seen:
                    continue
                seen.add((names[-1], norm(q)))
                segs = [x for x in (norm(y) for y in re.split(r"\.{3}|…", q)) if len(x.split()) >= 3] or [norm(q)]
                hits = [(fr, d) for fr, d, t in msgs if all(x in t for x in segs)]
                if not hits:
                    # 引用の中 (返信が引いた形) にしか無いか、cache に無い月の通。前者は帰属の確かめ先が返信の側に無い
                    tally["引用を除いた本文に無い"] += 1
                    out.append(f"[引用を除いた本文に無い] {os.path.relpath(f, root)}:{n}  {names[-1]} 氏 ← {q[:70]!r}")
                    continue
                name_ok = any(names[-1].lower() in fr.lower() for fr, _d in hits)
                year_ok = not years or any(d and str(d.year) == years[-1] for fr, d in hits if names[-1].lower() in fr.lower())
                if all("yuta.yokoi" in fr for fr, _d in hits):
                    kind = "我々の投稿にだけ在る (ACD の本文など)"
                elif not name_ok and not any(re.search(r"\(.*[A-Za-z].*\)", fr) for fr, _d in hits):
                    kind = "差出人の名がラテン文字でない (人が見る)"
                else:
                    kind = "一致" if name_ok and year_ok else "人名が違う" if not name_ok else "年が違う (同じ文の別の年を拾いやすい)"
                tally[kind] += 1
                if kind != "一致" and not kind.startswith("我々の投稿"):
                    got = sorted({f"{fr[:40]} {d.date() if d else '?'}" for fr, d in hits})[:3]
                    out.append(f"[{kind}] {os.path.relpath(f, root)}:{n}  {names[-1]} 氏{' ' + years[-1] if years else ''} ← "
                               f"{q[:70]!r}  / 通: {got}")
    print("帰属の照合: " + " / ".join(f"{k} {v}" for k, v in tally.most_common()))
    for o in out:
        print("  " + o)
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", nargs="*", metavar="FILE",
                    help="rounds の各通がアーカイブに逐語で在るかを当てる (FILE を省くと rounds/*.txt の全部)")
    ap.add_argument("--fetch", action="store_true", help="不足月をアーカイブから取得する")
    ap.add_argument("--root", default=".")
    ap.add_argument("--record-entry", action="store_true", help="入口の引用を全 corpus に当てて manifest を更新する")
    ap.add_argument("--all-italics", action="store_true", help="人名の近傍に限らず、斜体の引用をすべて当てる")
    ap.add_argument("--summaries", action="store_true", help="「要約」と書いた語句が原文に逐語で在るかを当てる")
    ap.add_argument("--attribution", action="store_true", help="逐語を含む通の差出人と年を、ドシエが帰属させた人名と年に当てる")
    args = ap.parse_args()
    if args.attribution:
        return attribution(args.root)
    if args.rounds is not None:
        return rounds(args.root, args.rounds)
    if args.summaries:
        return summaries(args.root)
    if args.record_entry:
        return record_entry(args.root)

    if stale_months():
        print(f"⚠ cache に欠けがある: {stale_months()}。その月の発言が未確認に落ちるので足す")
    quotes = collect_quotes(args.root, named=not args.all_italics)
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
        # **2 巡目は年で取る。** 月の導出は「節の中に `YYYY-MM` が書いてあること」に依存するが、
        # ドシエは *"submitted later that year"* のように**年しか書いていない**箇所がある
        # （2026-09-20 実測: Open Constitution License の引用がこれで永久に未確認だった）。
        # **書き手が月を書かなかったことが、道具の側では「出典に当たれていない」として出る。**
        if miss:
            n2 = fetch(needed_years(miss, args.root))
            print(f"  年単位でさらに {n2} file 取得して再照合")
            blob = load_sources(args.root)
            miss = {q: v for q, v in miss.items() if not present(q, blob)}
            print(f"  再照合後（年単位）: 確認できた {len(quotes) - len(miss)} / 確認できない {len(miss)}")

    # **残差を 2 つに割る。** 外部で確認できなかったもののうち、**自分の成果物に在る**ものは
    # 外部照合の対象ではない（自己引用）。**残りだけが「出典に当たれていない引用」である。**
    selfblob = load_self(args.root)
    selfq = {q: v for q, v in miss.items() if present(q, selfblob)}
    miss = {q: v for q, v in miss.items() if q not in selfq}
    print(f"  うち自己引用（外部照合の対象外）: {len(selfq)}")
    print(f"  出典に当たれていない引用: {len(miss)}")

    if miss:
        # ⚠ **見出しは実際に出す件数を述べること。** 2026-09-22 まで、この見出しは
        # 既定でも「未確認（全件）」と名乗りながら **15 件で打ち切っていた** ——
        # 読み手（実際に踏んだ）は 15 件を分類して「全部が自己引用の強調＝clean」と結論できる。
        # **`against.md` #180 はこの道具が残差を誤って報告する件だった。同じ族の 2 度目である。**
        _all = bool(os.environ.get("DOSSIER_ALL"))
        _shown = list(miss.items()) if _all else list(miss.items())[:15]
        if _all or len(_shown) == len(miss):
            print(f"\n--- 未確認（全 {len(miss)} 件） ---")
        else:
            print(f"\n--- 未確認（{len(miss)} 件中 {len(_shown)} 件のみ表示 / "
                  f"全件は DOSSIER_ALL=1） ---")
        for q, locs in _shown:
            print(f"  [{locs[0]}] {q[:110]}")
        print("\n**未確認 = 誤引用ではない。** 我々自身の文を強調で括ったものと、"
              "まだ取得していない月の両方が入る。**分類してから結論すること。**")
        near = near_misses(miss, blob)
        print(f"\n--- 前後だけ原文に一致する引用（{len(near)} 件・語を落とした誤引用はここに出る） ---")
        for score, loc, seg in near:
            print(f"  {score:.2f} [{loc}] {seg[:110]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
