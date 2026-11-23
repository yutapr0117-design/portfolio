#!/usr/bin/env python3
"""read_thread.py — census の会話 1 本を、引用行を除いて時刻順に出す (未読を読むための道具・2026-11-15・9b)。

**なぜ在るか**: オーナーの依頼「未読の OSI スレッドを 5 人で無くして、反映して」(2026-11-15)。census は会話を数えるが
本文を出さないので、各自がアーカイブの月の file から通を手で拾っていた。引用 (`>` と Outlook の Original Message) を
除くので、別人の文を発言者の文として引く誤り (1c が 11-15 に踏んだ) も減る。当て直しの輪番 (2f の提案 (B)) にも使う。

使い方 (repo の root で・DOSSIER_ARCHIVE_CACHE にアーカイブの写し):
    python3 read_thread.py --start 2002-03-13 --subject "OSD modification regarding what license can require of user"
    python3 read_thread.py ... --deciders-only     # 決める側の通と最初の通だけ
    python3 read_thread.py ... --max-words 400     # 1 通の語数の上限 (既定 600)
出すもの: 通ごとに [番号] 日付・差出人 (決める側には ★)・本文 (`>` で始まる引用行と署名の後を除く)。
最後に、通の数・決める側の通の数・語数。会話の切り方は census_decision_statements.conversations() と同じ。
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import census_decision_statements as c  # noqa: E402


def clean(body: str) -> str:
    out = []
    for ln in body.split("\n"):
        if ln.startswith("-- ") or ln.strip() in ("--", "-------------- next part --------------") \
                or re.match(r"\s*-{3,}\s*Original Message\s*-{3,}", ln, re.I):
            break  # 署名・添付・Outlook の形の引用 (">" の無い別人の文) から先は本人の文ではない
        if ln.lstrip().startswith(">") or re.match(r"^\s*On .{5,80} wrote:\s*$", ln) or re.match(r"^.{0,60} writes:\s*$", ln):
            continue
        out.append(ln)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True)
    ap.add_argument("--subject", required=True)
    ap.add_argument("--deciders-only", action="store_true")
    ap.add_argument("--max-words", type=int, default=600)
    o = ap.parse_args()
    key = c.title_key(o.subject)
    convs = c.conversations()
    hit = [g for k, v in convs.items() if k == key or k[:len(key)] == key for (d, _last, g) in v if d == o.start]
    if not convs:
        print("STOP: アーカイブの写しが読めない。DOSSIER_ARCHIVE_CACHE=<写しの dir> を付ける")
        return 2
    if not hit:
        print(f"STOP: 会話が見つからない: {o.start} {o.subject!r} (key {key!r})")
        return 2
    g = hit[0]
    n_dec = words = cut = 0
    for i, (_when, date, frm, _title, body, *_loc) in enumerate(g, 1):
        dec = c.is_decider(frm)  # アドレスと MIME の表示名も照らす (#3896 と同じ判定・2026-11-23)
        n_dec += dec
        if o.deciders_only and not dec and i != 1:
            continue
        txt = clean(body)
        w = txt.split()
        words += len(w)
        if len(w) > o.max_words:
            cut += 1
            txt = " ".join(w[:o.max_words]) + f" …[+{len(w) - o.max_words} 語]"
        name = re.sub(r"\s*<[^>]*>|\S+@\S+", "", frm).strip(' "()') or frm
        print(f"\n[{i}] {date[:31]} · {'★' if dec else ''}{name}\n{txt}")
    # 切った通の数を最後に出す (2026-11-16・30 の依頼): 2f と 9b は決める側の通を上限で切ったまま「論点なし」と読み、
    #   全文で読み直すと論点が出た。切ったことを末尾の 1 行で見えるようにする (出力の末尾だけを読んでも目に入る)
    print(f"\n# {o.start} {o.subject}: {len(g)} 通 (決める側 {n_dec}) · 出した本文 {words} 語"
          + (f" · ⚠ 上限 {o.max_words} 語で切った通 {cut} —— 論点の判断の前に全文で読む" if cut else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
