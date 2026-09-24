#!/usr/bin/env python3
"""OSI 両リストのアーカイブ全数から、スレッド単位の基準率を出す。

**CI には入れない** —— 外部フォーラムの定期取得は壊れやすい (CLAUDE.md §7)。
手で走らせる道具で、キャッシュ先は `DOSSIER_ARCHIVE_CACHE` と同じ形の
`<list>-<YYYY>-<Month>.txt` を並べたディレクトリ。

使い方:
    DOSSIER_ARCHIVE_CACHE=<dir> python3 .github/scripts/archive_census.py

**v1 は誤りだった（#228）**: RFC 5322 のヘッダ折り返しを無視し `Subject:` の 1 物理行
だけを読んだため、**同じスレッドが違う位置で折り返されると別題として割れた**。
#109 が同じ窓で 68 スレッドとしたのに対し v1 は 90 と数え、返信ゼロ率が
22% → 38.9% へ **我々に有利な向きに** 膨らんでいた。
**対照（新しい道具で既知の数字を再現してみる）だけがこれを教えた。**
"""
import os
import pathlib, re, collections, json, re, collections, json
from email.header import decode_header, make_header
SP = pathlib.Path(os.environ.get("DOSSIER_ARCHIVE_CACHE", "archive-cache"))
FROM = re.compile(r"^From .*\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b")

def unfold(lines, i):
    """折り返しを畳んでヘッダ値を返す。"""
    val = lines[i].split(": ", 1)[1] if ": " in lines[i] else ""
    j = i + 1
    while j < len(lines) and lines[j][:1] in (" ", "\t"):
        val += " " + lines[j].strip(); j += 1
    return val, j

def decode(s):
    try: return str(make_header(decode_header(s)))
    except Exception: return s

def norm(s):
    s = decode(s)
    s = re.sub(r"^\s*((re|aw|fwd|fw)\s*:\s*)+", "", s.strip(), flags=re.I)
    s = re.sub(r"\[license-(review|discuss)\]\s*", "", s, flags=re.I)
    s = re.sub(r"^\s*((re|aw|fwd|fw)\s*:\s*)+", "", s, flags=re.I)   # 接頭辞が括弧の内側に来る形
    return re.sub(r"\s+", " ", s).strip().lower()

def parse(p):
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    out, cur, i, inhdr = [], None, 0, False
    while i < len(lines):
        l = lines[i]
        if FROM.match(l):
            if cur: out.append(cur)
            cur = {"s": ""}; inhdr = True; i += 1; continue
        if inhdr and not l.strip(): inhdr = False
        if inhdr and cur is not None and not cur["s"] and l.startswith("Subject: "):
            cur["s"], i = unfold(lines, i); continue
        i += 1
    if cur: out.append(cur)
    return [m for m in out if m["s"]]

def run(lst, lo=0, hi=9999):
    MON = "January February March April May June July August September October November December".split()
    th, msgs, months = collections.defaultdict(int), 0, 0
    for p in sorted(SP.glob(f"{lst}-*.txt")):
        y = int(p.stem.split("-")[2])
        if not (lo <= y <= hi): continue
        months += 1
        for m in parse(p):
            th[norm(m["s"])] += 1; msgs += 1
    z = sum(1 for v in th.values() if v == 1)
    return months, msgs, len(th), z, (round(z/len(th)*100, 1) if th else 0)

print("=== 対照: #109 の窓に当てる（#109 は 30 か月 / 439 通 / 68 スレッド / 22%）===")
print("  license-discuss 2024-2026:", run("license-discuss", 2024, 2026))
print("\n=== 全数 ===")
res = {}
for lst in ("license-review", "license-discuss"):
    res[lst] = run(lst)
    mo, ms, t, z, r = res[lst]
    print(f"  {lst:16} {mo} か月 / {ms} 通 / {t} スレッド / 返信ゼロ {z} = {r}%")
print(json.dumps(res, ensure_ascii=False))
