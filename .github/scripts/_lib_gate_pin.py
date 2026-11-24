"""_lib_gate_pin.py — 出す版を替える前の最後の門 (議題 29 の丁・議題 31): 本文・一覧・指示文・門の文を固定し、動けば日数を数え直す。

LICENSES/ACD-<版>-GATE.md が持つもの: 門の文 (GATE-TEXT の間)・読み手へ渡す指示文 (GATE-PROMPT の間)・固定の印 (GATE-PIN)・
結果 (GATE-RESULT)。CI の Check 504 は、作業中の草案の版の GATE.md について、印の 4 つの sha がいまの草案の本文・CHANGES・門の文・
指示文と一致することと、結果が高々 1 つで、結果の後に数え直していないことを見る。確定の道具は、日数・結果・git の履歴 (印の since より
後に本文か一覧が動いていないか。CI は浅い履歴なので確定の側で見る) を見る。印を書き直す道具は `moved_clauses.py --pin`。
"""
from __future__ import annotations

import datetime
import hashlib
import re
import subprocess
from pathlib import Path

from moved_clauses import ROOT, body_sha, working_draft

PIN = re.compile(r"<!-- GATE-PIN: version=(?P<v>\d+\.\d+) since=(?P<since>\d{4}-\d{2}-\d{2}) days=(?P<days>\d+) body-sha256=(?P<body>[0-9a-f]{64}) "
                 r"changes-sha256=(?P<changes>[0-9a-f]{64}) text-sha256=(?P<text>[0-9a-f]{64}) prompt-sha256=(?P<prompt>[0-9a-f]{64}) -->")
RESULT = re.compile(r"<!-- GATE-RESULT: (?:none|date=(?P<date>\d{4}-\d{2}-\d{2}) unlisted-high=(?P<high>\d+) partly-high=(?P<partly>\d+) "
                    r"listed-high=(?P<listed>\d+) listed-high-agreed=(?P<agreed>\d+) reports=(?P<reports>\S+)) -->")
# 門の文が持つこと (議題 29 の丁・議題 31 の条件 1)。文を薄めた門を「同じ門」と呼ばせない
MUST_SAY = ("結果を見た後に選んだ門", "落ちたら", "1.4 のまま", "3 つ目の門は作らない", "1 回だけ", "PARTLY LISTED", "全員一致", "別の agent")


def failed(r: re.Match) -> bool:
    """結果が不合格か: 一覧に無い HIGH・PARTLY LISTED の HIGH が 1 以上、または一覧に在る HIGH に全員一致で残すと決めていないものがある。"""
    return bool(int(r["high"]) or int(r["partly"]) or int(r["listed"]) != int(r["agreed"]))


def _block(text: str, tag: str) -> str | None:
    m = re.findall(rf"<!-- {tag} -->\n(.*?)\n<!-- /{tag} -->", text, re.S)
    return m[0] if len(m) == 1 else None


def _sha(s: str) -> str:
    return hashlib.sha256(" ".join(s.split()).encode()).hexdigest()


def gate_file(v: str) -> Path:
    return ROOT / "LICENSES" / f"ACD-{v}-GATE.md"


def current(v: str, gate_text: str) -> dict[str, str]:
    """いまの 4 つの sha。"""
    draft = (ROOT / "LICENSES" / f"ACD-{v}-DRAFT.txt").read_text(encoding="utf-8")
    changes = ROOT / "LICENSES" / f"CHANGES-ACD-{v}.txt"
    return {"body": body_sha(draft), "changes": _sha(changes.read_text(encoding="utf-8")) if changes.exists() else "",
            "text": _sha(_block(gate_text, "GATE-TEXT") or ""), "prompt": _sha(_block(gate_text, "GATE-PROMPT") or "")}


def pin_problems(v: str) -> list[str] | None:
    """Check 504 の本体。GATE.md が無ければ None (門を置いていない版)。"""
    f = gate_file(v)
    if not f.exists():
        return None
    t = f.read_text(encoding="utf-8")
    text, prompt = _block(t, "GATE-TEXT"), _block(t, "GATE-PROMPT")
    if text is None or prompt is None:
        return ["門の文 (GATE-TEXT) か指示文 (GATE-PROMPT) の区切りが 1 組でない"]
    out = [f"門の文に「{w}」が無い" for w in MUST_SAY if w not in text]
    pins, results = list(PIN.finditer(t)), list(RESULT.finditer(t))
    if not pins and t.count("<!-- GATE-PIN: pending -->") == 1 and len(results) == 1 and not results[0]["date"]:
        return out  # まだ数え始めていない (門の文の必須の句だけを見る。確定の道具は印が無いので止まる)
    if len(pins) != 1 or len(results) != 1:
        return out + [f"印 (GATE-PIN) が {len(pins)} 個・結果 (GATE-RESULT) が {len(results)} 個 (どちらも 1 個。結果は 1 回だけ)"]
    p, r = pins[0], results[0]
    if p["v"] != v:
        out.append(f"印の版 {p['v']} が {v} でない")
    if r["date"]:
        # 門は終わった: 合否は確定の道具が見る。読んだものが固定したものと違う (結果の後に数え直した) なら止める
        if r["date"] < p["since"]:
            out.append("結果の日が固定の日より前 (結果を見た後に固定し直している。読みは 1 回だけ)")
        elif (datetime.date.fromisoformat(r["date"]) - datetime.date.fromisoformat(p["since"])).days < int(p["days"]):
            out.append(f"固定から {p['days']} 日たつ前に読んでいる")
        if not (ROOT / r["reports"]).exists():
            out.append(f"結果の報告 {r['reports']} が無い")
        if failed(r):
            return out  # 落ちた門: 草案は次の版のために動いてよいので sha は照らさない (確定は gate_problems が止める)
    now = current(v, t)
    out += [f"{k}-sha256 がいまの{n}と違う (動かしたら `moved_clauses.py --pin` で日数を数え直す)"
            for k, n in (("body", "草案の本文"), ("changes", "変更の一覧"), ("text", "門の文"), ("prompt", "指示文")) if p[k] != now[k]]
    return out


def _moved_after(v: str, since: str) -> list[str]:
    """印の since (UTC の日) より後に書かれた commit (author の日。rebase merge は committer の日を替える) で、本文か一覧の中身が動いていればその file。"""
    out = []
    for rel, sha in ((f"LICENSES/ACD-{v}-DRAFT.txt", body_sha), (f"LICENSES/CHANGES-ACD-{v}.txt", _sha)):
        log = subprocess.run(["git", "log", "--format=%H %aI", "--", rel], cwd=ROOT, text=True, capture_output=True).stdout.split("\n")
        now = sha((ROOT / rel).read_text(encoding="utf-8"))
        for ln in filter(None, log):
            h, at = ln.split()
            day = datetime.datetime.fromisoformat(at).astimezone(datetime.timezone.utc).date().isoformat()
            if day <= since:
                break
            parent = subprocess.run(["git", "show", f"{h}^:{rel}"], cwd=ROOT, text=True, capture_output=True)
            if parent.returncode != 0 or sha(parent.stdout) != now:
                out.append(f"{rel} が {day} ({h[:8]}) に動いた")
                break
    return out


def gate_problems(v: str, today: datetime.date | None = None) -> list[str]:
    """確定の道具の門: 印・日数・結果・履歴。"""
    today = today or datetime.datetime.now(datetime.timezone.utc).date()
    bad = pin_problems(v)
    if bad is None:
        return [f"{gate_file(v).name} が無い (出す版を替える前の門・議題 29 の丁)"]
    t = gate_file(v).read_text(encoding="utf-8")
    p, r = PIN.search(t), RESULT.search(t)
    if not p or not r:
        return bad + ["固定の印 (GATE-PIN) がまだ打たれていない"]
    left = (datetime.date.fromisoformat(p["since"]) + datetime.timedelta(days=int(p["days"])) - today).days
    if left > 0:
        bad.append(f"固定 ({p['since']}) から {p['days']} 日のうち、あと {left} 日残っている")
    bad += _moved_after(v, p["since"])
    if not r["date"]:
        bad.append("読みの結果 (GATE-RESULT) が無い")
    elif failed(r):
        bad.append(f"門に落ちている (一覧に無い HIGH {r['high']}・PARTLY LISTED の HIGH {r['partly']}・一覧に在る HIGH {r['listed']} のうち全員一致で"
                   f"残すもの {r['agreed']})。出す版は替えず、3 つ目の門は作らない")
    return bad


def repin(today: datetime.date | None = None) -> str:
    """印の 4 つの sha と since を、いまの草案・一覧・文で書き直す (動かした日に数え直す)。結果が在れば書き直さない。"""
    d = working_draft()
    v = re.match(r"ACD-(\d+\.\d+)-DRAFT", d.name).group(1)
    f = gate_file(v)
    t = f.read_text(encoding="utf-8")
    r = RESULT.search(t)
    if r and r["date"]:
        raise SystemExit("結果 (GATE-RESULT) が在る。読みは 1 回だけなので、数え直さない")
    p = PIN.search(t)
    now = current(v, t)
    day = (today or datetime.datetime.now(datetime.timezone.utc).date()).isoformat()
    if p and all(p[k] == now[k] for k in now):
        return f"動いていない (since={p['since']} のまま)"
    days = p["days"] if p else "7"
    new = (f"<!-- GATE-PIN: version={v} since={day} days={days} body-sha256={now['body']} changes-sha256={now['changes']} "
           f"text-sha256={now['text']} prompt-sha256={now['prompt']} -->")
    t = PIN.sub(new, t, 1) if p else t.replace("<!-- GATE-PIN: pending -->", new, 1)
    f.write_text(t, encoding="utf-8")
    return f"固定した: since={day}"
