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
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

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
    return _check_assets(html)


def _wellknown_paths():
    """`.well-known/` 配下の tracked file を **導出**する (ハードコードは追加時に drift する)。

    ここが dot-directory の canary になる: GitHub Pages の Jekyll 処理は `.` / `_` で始まる
    ディレクトリを配信対象から落とすため、`.nojekyll` が失われると **`.well-known/` が丸ごと
    404 になる**。リポジトリ側の Check は `.nojekyll` という *file の存在* を見るだけで、
    その *効果* は見ていない。AIO 層はこのプロジェクトの中核資産なので、効果の方を測る。
    """
    try:
        out = subprocess.run(["git", "ls-files", ".well-known"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout
    except Exception:  # noqa: BLE001 — git が無い環境では canary を諦める (index.html 由来は残る)
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]


def _same_origin_refs(html, base):
    """公開 index.html が宣言している同一オリジンの参照を集める。"""
    refs = set()
    for m in re.finditer(r'(?:href|src)="([^"]+)"', html):
        refs.add(m.group(1))
    for m in re.finditer(r'<meta[^>]+content="(https://[^"]+)"', html):
        refs.add(m.group(1))
    out = []
    for r in sorted(refs):
        if r.startswith(("#", "data:", "mailto:", "tel:")):
            continue
        if r.startswith("http") and not r.startswith(base.split("/portfolio/")[0]):
            continue
        out.append(r)
    return out


def _sitemap_locs(base):
    """公開 sitemap.xml が宣言している URL を集める。

    WHY 別枠にするか — **`.md` が raw で配信される契約の canary** だから。
    Jekyll は `.md` を HTML へ変換して URL を変えてしまう (`README.md` → `README.html`) ので、
    `.nojekyll` が失われると **sitemap が指す `.md` が軒並み 404 になる**。これは
    `.well-known/` が消える dot-directory の失敗とは別の経路で、しかも sitemap には
    `AI2AI.md` / `README.md` / `docs/evidence/real-work-claims.md` など **AI クローラ向けの
    権威面**が並んでいる = このプロジェクトの中核賭け金が丸ごと届かなくなる。

    リポジトリ側は Check 386 が「`<loc>` が実在ファイルへ解決する」ことを既に強制している。
    ここで測るのは *配信されているか* という別の層 (存在 ≠ 配信)。
    """
    try:
        req = urllib.request.Request(base + "sitemap.xml", headers={
            "Cache-Control": "no-cache",
            "User-Agent": "portfolio-deployed-freshness-check",
        })
        with urllib.request.urlopen(req, timeout=30) as r:
            xml = r.read().decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        print(f"::error::公開 sitemap.xml を取得できない ({type(e).__name__}: {e})", flush=True)
        return ["sitemap.xml"]  # 到達不能そのものを違反として下流に流す
    # `<image:loc>` ではなくページの `<loc>` のみ。fragment はサーバへ送られないので落とす。
    return [loc.split("#")[0] for loc in re.findall(r"<loc>([^<]+)</loc>", xml)]


def _check_assets(html):
    """**宣言されている資産が実際に配信されているか**を測る。

    WHY: リポジトリ側の Check 群は「file がリポジトリに存在するか」「参照が repo 内で解決するか」
    を見るが、**配信されているか**は誰も見ていない。Pages の設定変更や `.nojekyll` の喪失で
    一部のパスだけが 404 になっても、全ゲートが緑のまま公開面だけが壊れる。
    """
    base = _site_url()
    targets = _same_origin_refs(html, base) + _wellknown_paths() + _sitemap_locs(base)
    seen, bad = set(), []
    for ref in targets:
        url = urljoin(base, ref)
        if url in seen:
            continue
        seen.add(url)
        try:
            rq = urllib.request.Request(url, headers={
                "Cache-Control": "no-cache",
                "User-Agent": "portfolio-deployed-freshness-check",
            })
            with urllib.request.urlopen(rq, timeout=30) as resp:
                if resp.status != 200:
                    bad.append((ref, resp.status))
        except urllib.error.HTTPError as e:
            bad.append((ref, e.code))
        except Exception as e:  # noqa: BLE001
            bad.append((ref, type(e).__name__))

    if bad:
        for ref, code in bad:
            print(f"::error::公開サイトで解決しない参照: {ref} ({code})", flush=True)
        print("::error::index.html が宣言している資産 (と .well-known 配下) が配信されていない。"
              "`.nojekyll` が失われると Jekyll 処理が `.` で始まるディレクトリを落とすため "
              "**.well-known/ が丸ごと 404 になる** — リポジトリ側の Check は file の存在しか"
              "見ないのでこの失敗は全ゲート緑のまま起きる", flush=True)
        return 1

    print(f"OK: 公開サイトが宣言している資産 {len(seen)} 件 "
          "(index.html の参照 ∪ .well-known ∪ sitemap の <loc>) がすべて 200 で配信されている")
    rc = _check_shipped_bytes(base)
    return rc or _check_module_mime(base) or _check_digests(base)


def _check_module_mime(base):
    """動的 import される module が **JS の MIME で配信されている**ことを確かめる。

    [FIX 2026-08-21] quiz の問題集データは静的 import から **動的 import** へ移した
    (#1239・クリティカルパスから 130,595 bytes を外すため)。動的 import は仕様上
    **MIME が JavaScript でないと即座に失敗する** —— `text/plain` や `application/octet-stream`
    で返ると module は評価されず、利用者から見ると「問題集がいつまでも読み込めない」になる。

    この失敗モードは **どの層も見ていなかった**:
      - リポジトリ側の Check   … ローカルの file しか見ない (MIME は配信側の性質)
      - behavior e2e           … ローカルの http-server が返す MIME を見ているだけ
      - `_check_shipped_bytes` … 中身の sha256 は見るが **ヘッダは見ない**
    静的 import 時代は index.html の `<script type="module">` 経由でまとめて読まれ、
    かつ modulepreload もあったので MIME 事故は起きにくかったが、動的 import では
    **その module 単体の MIME だけ**が効く。

    実測 (2026-08-21): GitHub Pages は `application/javascript; charset=utf-8` を返す。
    """
    targets = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "js" / "quiz").glob("*.js"))
    bad = []
    for name in targets:
        try:
            rq = urllib.request.Request(base + name, headers={
                "Cache-Control": "no-cache",
                "User-Agent": "portfolio-deployed-freshness-check",
            })
            with urllib.request.urlopen(rq, timeout=30) as resp:
                ctype = (resp.headers.get("Content-Type") or "").lower()
        except Exception as e:  # noqa: BLE001
            bad.append((name, type(e).__name__))
            continue
        # HTML 仕様の "JavaScript MIME type essence match"
        if not any(ctype.startswith(t) for t in (
                "text/javascript", "application/javascript", "application/ecmascript",
                "text/ecmascript", "application/x-javascript")):
            bad.append((name, f"MIME が JS でない: {ctype!r}"))

    if bad:
        for name, why in bad:
            print(f"::error::動的 import される {name} の MIME が不正 — {why}", flush=True)
        print("::error::動的 import は **MIME が JavaScript でないと即座に失敗する**。"
              "利用者から見ると「問題集がいつまでも読み込めない」になるが、"
              "リポジトリ側の Check も behavior e2e も配信ヘッダを見ないので全ゲート緑のまま起きる",
              flush=True)
        return 1

    if not targets:
        print("::error::動的 import 対象 (js/quiz/*.js) が 1 つも見つからない — "
              "走査先が変わったなら _check_module_mime の対象も追従せよ", flush=True)
        return 1

    print(f"OK: 動的 import される module {len(targets)} 件が JS の MIME で配信されている")
    return 0


def _check_shipped_bytes(base):
    """shipped な CSS/JS が **リポジトリと同じ中身** で配信されているかを検証する。

    上の資産チェックは **200 が返るかしか見ていない**。だが「200 は返るが中身が古い」は
    別の失敗モードで、部分デプロイ / CDN キャッシュ混線で普通に起こりうる。実害は重い ——
    例えば style.css だけ古いままだと、直したはずのコントラストや focus の契約が
    **公開面では効いていない**のに、リポジトリ側の Check も behavior e2e も
    (ローカルの成果物を見ているので) すべて緑のままになる。

    AIO 面 (llms.txt 等) は `_check_digests` が sha256 で見ているので、同じ考えを
    **shipped 面へ広げる**。

    [FIX] 対象は shipped な **全** JS + CSS。以前は style.css / main.js / sw.js の 3 件だけで、
    その根拠を「全 js/*.js を舐めると週次ジョブが遅くなる / 中核が一致していれば部分デプロイは
    ほぼ確実に検出できる」と書いていたが、**どちらも実測で反証された** (2026-08-21):

      - 所要: 全 37 件を fetch + sha256 して **4.1 秒**。週次ジョブに対して無視できる。
      - 被覆: Stage 5 で main.js は 7,785 → 1,000 行台まで縮み、ロジックは
        **34 個の葉モジュールへ移った**。つまり「中核 3 件が一致していれば安心」は
        抽出が進むほど成り立たなくなる前提だった。例えば js/store.js (全 ingestion が
        通る正規化) や js/settings-io.js (バックアップの入出力) が古いまま配信されても、
        index.html も main.js も style.css も一致するので **検出できない**。
        サイトは普通に読み込めてしまい、リポジトリ側の Check も behavior e2e も
        (ローカルの成果物を見ているので) 緑のまま = 完全に silent。

    「一般論を根拠にコードを足すな / 削るな —— 必要性は実測で示せ」(CLAUDE.md §7) を
    自分たちの rationale にも適用した結果の是正。
    """
    import hashlib

    targets = ["style.css", "main.js", "sw.js"] + sorted(
        str(p.relative_to(ROOT)) for p in
        list((ROOT / "js").glob("*.js")) + list((ROOT / "js" / "quiz").glob("*.js"))
    )
    bad = []
    for name in targets:
        local = ROOT / name
        if not local.exists():
            bad.append((name, "リポジトリに無い"))
            continue
        want = hashlib.sha256(local.read_bytes()).hexdigest()
        try:
            rq = urllib.request.Request(base + name, headers={
                "Cache-Control": "no-cache",
                "User-Agent": "portfolio-deployed-freshness-check",
            })
            with urllib.request.urlopen(rq, timeout=30) as resp:
                got = hashlib.sha256(resp.read()).hexdigest()
        except Exception as e:  # noqa: BLE001
            bad.append((name, type(e).__name__))
            continue
        if got != want:
            bad.append((name, f"sha256 不一致 deployed={got[:12]} repo={want[:12]}"))

    if bad:
        for name, why in bad:
            print(f"::error::公開されている {name} がリポジトリと違う — {why}", flush=True)
        print("::error::200 が返ることと『中身が最新であること』は別の失敗モード。"
              "部分デプロイ / キャッシュ混線でこの状態になると、直したはずの契約が"
              "**公開面だけ効いていない**のにリポジトリ側の Check も e2e も緑のままになる", flush=True)
        return 1

    print(f"OK: shipped な中核資産 {len(targets)} 件が sha256 でリポジトリと一致している")
    return 0


def _fetch_bytes(url):
    req = urllib.request.Request(url, headers={
        "Cache-Control": "no-cache",
        "User-Agent": "portfolio-deployed-freshness-check",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def _check_digests(base):
    """**配信されたバイト列が宣言どおりの中身か**を検証する。

    デプロイの失敗モードは 3 段ある。ここは 3 段目:
      1. ジョブが失敗する                  → pages-build-deployment のバッジ (Check 415)
      2. 版数が古い / 資産が届かない        → 本 script の前段 (#1004 / #1005 / #1009)
      3. **届いた中身が宣言と違う**          ← ここ

    AIO 層は `.well-known/aio-manifest.json` と `.well-known/agent-skills/index.json` で
    **sha256 を公開している**。整合性を検証するエージェントは digest が合わなければ資源を
    棄却するので、配信側でバイト列が変質すると (Pages の変換・部分デプロイ・キャッシュ混線)
    **200 は返るのに AIO 層だけが機能しない**。リポジトリ側の `check_aio_digests.py` は
    ローカルのファイルしか見ないため、この層は別途必要になる。

    テキスト資産のみを対象にする (binary は同じ URL 検証を前段が済ませており、
    数 MB を毎週取り直す価値が薄い)。
    """
    targets = []  # (label, url, expected_sha256)
    try:
        skills = json.loads(_fetch_bytes(base + ".well-known/agent-skills/index.json").decode("utf-8"))
        for sk in skills.get("skills", []):
            dg = str(sk.get("digest", ""))
            if dg.startswith("sha-256:"):
                targets.append((f"agent-skills/{sk.get('name')}", sk["url"], dg.split(":", 1)[1]))
    except Exception as e:  # noqa: BLE001
        print(f"::error::公開 agent-skills/index.json を読めない ({type(e).__name__}: {e})", flush=True)
        return 1

    try:
        manifest = json.loads(_fetch_bytes(base + ".well-known/aio-manifest.json").decode("utf-8"))
        for key in ("source_of_truth", "supporting_evidence", "observational_evidence"):
            for entry in manifest.get(key, []):
                path = str(entry.get("path", ""))
                sha = str(entry.get("sha256", ""))
                if not path or not sha or not path.lower().endswith((".txt", ".md", ".json")):
                    continue
                targets.append((f"{key}/{path}", base + path, sha))
    except Exception as e:  # noqa: BLE001
        print(f"::error::公開 aio-manifest.json を読めない ({type(e).__name__}: {e})", flush=True)
        return 1

    bad = []
    for label, url, expected in targets:
        try:
            actual = hashlib.sha256(_fetch_bytes(url)).hexdigest()
        except Exception as e:  # noqa: BLE001
            bad.append(f"{label}: 取得できない ({type(e).__name__})")
            continue
        if actual != expected:
            bad.append(f"{label}: declared={expected[:16]}… actual={actual[:16]}…")

    if bad:
        for b in bad:
            print(f"::error::配信されたバイト列が宣言 digest と一致しない — {b}", flush=True)
        print("::error::整合性を検証する AI エージェントはこの資源を棄却する。200 は返るのに "
              "AIO 層だけが機能しない状態で、リポジトリ側の check_aio_digests.py では捕捉できない", flush=True)
        return 1

    print(f"OK: 公開されたテキスト資産 {len(targets)} 件が宣言 digest と一致している")
    return 0


if __name__ == "__main__":
    sys.exit(main())
