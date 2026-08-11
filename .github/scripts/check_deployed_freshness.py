#!/usr/bin/env python3
"""
check_deployed_freshness.py — 公開サイトがリポジトリと同じ版を配信しているかを検証する。

【なぜ必要か】
デプロイ連鎖には「ジョブが成功したか」と「配信されている中身が現在のものか」という
**別々の失敗モード**がある。前者は pages-build-deployment のバッジ (STATUS.md・Check 415) が
見ているが、後者を見ている層は 2026-08-11 時点でどこにも無かった:

  - PR ゲート (architecture-validation / playwright) は **ローカルの http-server** に対して走る。
    公開サイトを一度も触らない。
  - Check 2 / 17 / 180 は main.js の SITE_CONFIG と index.html の meta が**リポジトリ内で**
    一致することしか見ない。両方が正しくても配信が古ければ気付けない。
  - aio-monitoring.yml は AI エンジンへの問い合わせログを取るだけで、版数を照合しない。

つまり「Pages が数週間前から古い成果物を配信し続けている」状態が、**全ゲート緑のまま**
成立しうる。リポジトリが本体でサイトは付属物という位置づけでも、機能性 (loads / displays /
comprehensible) は死守する契約 (CLAUDE.md §3(B)) なので、配信の陳腐化は検出できねばならない。

【何を比べるか — なぜこの 2 つか】
`SITE_CONFIG.VERSION` と `SITE_CONFIG.LAST_UPDATED` を、公開 index.html の
`<meta name="ai:version">` / `<meta name="ai:last-modified">` と比較する。

この 2 つは **明示的な版数更新のときしか変わらない** (Version Update Checklist を通す)。
コミット SHA のような「毎回変わる値」を比べると、merge の直後に走ったときデプロイ完了前で
必ず落ちる = 週次バッジが恒常的に赤くなり、**赤が意味を持たなくなる**。逆にこの 2 つなら
「数週間デプロイが壊れている」という本当に知りたい状態だけが赤くなる。

【失敗の扱い】
ネットワーク失敗はリトライしたうえで**失敗として扱う**。週次実行なので、一時的な瞬断より
「公開サイトに到達できない状態が続いている」ことの方が重大で、それこそ知りたい情報だから。
"""
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ATTEMPTS = 3
BACKOFF_SEC = 5


def _repo_values():
    """main.js の SITE_CONFIG から期待値を取る (Check 2/17 が index.html との一致を保証済)。"""
    src = (ROOT / "main.js").read_text(encoding="utf-8")
    version = re.search(r"VERSION:\s*'([^']+)'", src)
    updated = re.search(r"LAST_UPDATED:\s*'([^']+)'", src)
    if not version or not updated:
        print("::error::main.js の SITE_CONFIG から VERSION / LAST_UPDATED を読めない", flush=True)
        sys.exit(1)
    return version.group(1), updated.group(1)


def _site_url():
    """canonical URL は CLAUDE.md から導出する (ハードコードは drift する)。"""
    m = re.search(r"https://[\w-]+\.github\.io/[\w-]+/", (ROOT / "CLAUDE.md").read_text(encoding="utf-8"))
    if not m:
        print("::error::CLAUDE.md から canonical site URL を導出できない", flush=True)
        sys.exit(1)
    return m.group(0)


def _fetch(url):
    last = None
    for i in range(ATTEMPTS):
        try:
            req = urllib.request.Request(url, headers={
                # Cache-Control: no-cache — CDN の中間キャッシュ越しに古い成果物を掴むと
                # 「デプロイが壊れている」と「キャッシュが残っている」を区別できない。
                "Cache-Control": "no-cache",
                "User-Agent": "portfolio-deployed-freshness-check",
            })
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001 — 種類を問わずリトライ対象
            last = e
            if i < ATTEMPTS - 1:
                time.sleep(BACKOFF_SEC * (i + 1))
    print(f"::error::公開サイトを {ATTEMPTS} 回取得できなかった ({type(last).__name__}: {last}) — "
          "一時的な瞬断ではなく到達不能が続いている可能性がある", flush=True)
    sys.exit(1)


def main():
    want_version, want_updated = _repo_values()
    url = _site_url() + "index.html"
    html = _fetch(url)

    got = {}
    for key in ("ai:version", "ai:last-modified"):
        m = re.search(r'<meta[^>]+name="%s"[^>]+content="([^"]+)"' % re.escape(key), html)
        got[key] = m.group(1) if m else None

    print(f"deployed: {url}")
    print(f"  ai:version       = {got['ai:version']!r}  (repo: {want_version!r})")
    print(f"  ai:last-modified = {got['ai:last-modified']!r}  (repo: {want_updated!r})")

    problems = []
    if got["ai:version"] is None or got["ai:last-modified"] is None:
        problems.append("公開 index.html に ai:version / ai:last-modified の meta が見つからない "
                        "(配信されているのが別の成果物か、meta が失われている)")
    else:
        if got["ai:version"] != want_version:
            problems.append(f"ai:version が古い: deployed={got['ai:version']} / repo={want_version}")
        if got["ai:last-modified"] != want_updated:
            problems.append(f"ai:last-modified が古い: deployed={got['ai:last-modified']} / repo={want_updated}")

    if problems:
        for p in problems:
            print(f"::error::公開サイトがリポジトリと同じ版を配信していない — {p}", flush=True)
        print("::error::pages-build-deployment のジョブが成功していても、配信されている中身が "
              "古ければこうなる (両者は別の失敗モード)。Pages の設定とデプロイ履歴を確認せよ", flush=True)
        return 1

    print("OK: 公開サイトはリポジトリと同じ版を配信している")
    return 0


if __name__ == "__main__":
    sys.exit(main())
