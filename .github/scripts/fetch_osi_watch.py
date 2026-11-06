#!/usr/bin/env python3
"""OSI の監視対象 9 URL を 1 回取り、前回との差を出す (手で回す道具・CI には入れない)。

    python3 .github/scripts/fetch_osi_watch.py [保存先]      # 既定は ~/osi-fetch/watch

外部情報は Mac で動くセッションしか取れない (`PEER-REVIEW-WATCH.md`)。日次の取得は 10-30 に、取得役の
session の終了とともに止まった。手順が session の中にしか無かったからなので、ここに置く。
opensource.org は一括取得で Cloudflare に遮断された実害があるので 1 並列・8 秒間隔で、URL を足さない。
分析はしない。変化があれば生データの場所を portfolio-00 の持ち分 (register) へ渡す。
"""
from __future__ import annotations

import datetime
import hashlib
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
LIST = "https://lists.opensource.org/pipermail/license-{}_lists.opensource.org/{}.txt"
JST = datetime.timezone(datetime.timedelta(hours=9))


def targets(now: datetime.datetime) -> list[tuple[str, str]]:
    """両リストの今月と先月、opensource.org の 5 ページ。月は実行日から導出する。"""
    first = now.replace(day=1)
    months = [(first - datetime.timedelta(days=1)).strftime("%Y-%B"), now.strftime("%Y-%B")]
    out = [(f"license-{name}_{m}.txt", LIST.format(name, m)) for name in ("review", "discuss") for m in months]
    out += [(f"oso_{n}", f"https://opensource.org/{p}") for n, p in (
        ("code-of-conduct.html", "code-of-conduct"), ("codeofconduct.html", "codeofconduct"),
        ("minutes.html", "minutes"), ("api_licenses.json", "api/licenses"), ("blog.html", "blog"))]
    return out


def summarize(name: str, data: bytes) -> str:
    """ページの生成で揺れる byte ではなく、変わったら意味のある値を返す。"""
    text = data.decode("utf-8", "replace")
    if "conduct" in name:
        found = re.findall(r"Last modified on [A-Za-z]+ \d+, \d+", text)
        return found[0] if found else "Last modified が無い"
    if name == "oso_minutes.html":
        return max(re.findall(r"meeting-minutes/(\d{4}-\d{2}-\d{2})", text), default="議事録の link が無い")
    if name == "oso_blog.html":
        return max(re.findall(r'published" datetime="([^"]+)"', text), default="記事の日付が無い")
    return hashlib.sha256(data).hexdigest()[:8]


def main() -> int:
    root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path.home() / "osi-fetch" / "watch"
    now = datetime.datetime.now(JST)
    day = root / now.strftime("%Y-%m-%d")
    day.mkdir(parents=True, exist_ok=True)
    base_path = root / "baseline.json"
    base = json.loads(base_path.read_text(encoding="utf-8")) if base_path.exists() else {}
    current: dict[str, str] = {}
    for name, url in targets(now):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40) as r:
                data = r.read()
            (day / name).write_bytes(data)
            current[name] = summarize(name, data)
        except urllib.error.HTTPError as e:
            current[name] = f"HTTP {e.code}"  # 月の最初の投稿が来るまで今月のページは 404 になる
        except OSError as e:
            current[name] = f"取得失敗 {type(e).__name__}"
        time.sleep(2 if "lists." in url else 8)
    print("取得", now.strftime("%Y-%m-%d %H:%M JST"), "保存先", day)
    for name, value in current.items():
        print(f"  {name}: {value}")
    failed = [n for n, v in current.items() if v.startswith("取得失敗") or v == "HTTP 403"]
    changed = {n: (base.get(n), v) for n, v in current.items() if n in base and base[n] != v}
    new = [n for n in current if n not in base]
    print("変化:", json.dumps(changed, ensure_ascii=False) if changed else "なし", "/ 新しい対象:", new or "なし")
    if failed:
        print("⚠ 取れなかったものがある。取れなかったことは世界についての証拠ではない:", failed)
    (day / "summary.json").write_text(json.dumps(current, ensure_ascii=False, indent=1), encoding="utf-8")
    good = {n: v for n, v in current.items() if n not in failed}
    base_path.write_text(json.dumps({**base, **good}, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
