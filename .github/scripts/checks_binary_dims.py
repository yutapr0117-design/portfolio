"""
checks_binary_dims.py — binary asset dimension/format + gate-workflow trigger checks (338/339/340/348)
(extracted from check_repository_consistency.py — check.py split track).

run(ctx) receives shared check()/ROOT/read/extract by reference (exec 不使用) so exit code / BLOCKING
propagation are byte-equivalent. 各 Check は対象 file を自前 read。annotation+def-aware free-var 確認済。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  338. `<meta property="og:image:width">` / `og:image:height` declared
       values MUST equal the ACTUAL pixel dimensions of the hero WebP
       (parsed directly from the VP8X/VP8/VP8L chunk header — no external
       library). Drift = the hero image is re-exported at a different
       resolution but the meta tags are not updated; social-card
       consumers that trust the declared dimensions render the card with
       a wrong aspect ratio (letterboxing / cropping) or reject the image.
       Check 298 verifies the values are positive integers but not that
       they match reality. Sibling of Check 298 (og:image dims positive
       int) / Check 337 (magic bytes) for the hero-image dimension-truth
       axis. (BLOCKING)

  339. Every JSON-LD `ImageObject` for the hero WebP that declares
       `width` / `height` MUST match the ACTUAL pixel dimensions of the
       hero WebP file. Drift = the image is re-exported at a new
       resolution and og:image (Check 338) gets updated but the JSON-LD
       ImageObject width/height stays stale — AI crawlers / knowledge
       graphs then ingest a wrong dimension for the entity's primary
       image. (This Check was born from a real drift found 2026-07-04:
       JSON-LD declared 1200x630 while the file was 1536x1024, corrected
       under C6 orchestrator approval.) Sibling of Check 338 (og:image
       dims == actual) for the JSON-LD ImageObject dimension-truth axis.
       (BLOCKING)

  340. Every JSON-LD `ImageObject` / `AudioObject` `encodingFormat` MIME
       for the hero WebP / BGM MP3 MUST match the ACTUAL binary format
       (webp→`image/webp`, mp3→`audio/mpeg`, from magic bytes). Drift =
       the JSON-LD declares a MIME (`image/png`, `audio/wav`) that
       disagrees with the real bytes — AI crawlers ingest a wrong
       content-type for the entity's primary media, and consumers that
       trust the declared MIME mis-decode. Check 337 verifies the magic
       bytes match the extension; this closes the JSON-LD MIME leg of the
       same truth. Sibling of Check 337 (magic bytes) / Check 339 (JSON-LD
       dims) for the binary-asset declaration-truth axis. (BLOCKING)

  348. Both BLOCKING gate workflows (`architecture-validation.yml` and
       `playwright-regression.yml`) MUST declare a `pull_request` trigger
       targeting the `main` branch in their `on:` block. This completes
       the meta-guard family: Check 346/347 verify the gates are INVOKED
       and BLOCKING, but a workflow whose `pull_request:` trigger is
       removed simply never runs on PRs — the `run:` step is present yet
       never executes, so PRs merge un-gated while CI shows no failure
       (there is nothing to fail). Sibling of Check 346 (consistency
       invocation) / Check 347 (behavior invocation) for the
       CI-triggers-the-guard axis. (BLOCKING)

"""
import re
import json
from pathlib import Path


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    read = ctx.read
    extract = ctx.extract

    # ── 338. og:image:width/height == actual hero WebP dimensions (BLOCKING) ─────
    def _parse_webp_dims338(_path):
        """外部ライブラリ不要で WebP の pixel 寸法を先頭 chunk から parse。"""
        _b = _path.read_bytes()[:40]
        if _b[0:4] != b"RIFF" or _b[8:12] != b"WEBP":
            return None
        _fourcc = _b[12:16]
        if _fourcc == b"VP8X":
            _w = 1 + int.from_bytes(_b[24:27], "little")
            _h = 1 + int.from_bytes(_b[27:30], "little")
            return (_w, _h)
        if _fourcc == b"VP8 ":
            _w = int.from_bytes(_b[26:28], "little") & 0x3FFF
            _h = int.from_bytes(_b[28:30], "little") & 0x3FFF
            return (_w, _h)
        if _fourcc == b"VP8L":
            _bits = int.from_bytes(_b[21:25], "little")
            _w = (_bits & 0x3FFF) + 1
            _h = ((_bits >> 14) & 0x3FFF) + 1
            return (_w, _h)
        return None

    _webp338 = ROOT / "yuta-yokoi-ai-pm-orchestration-system.webp"
    _html338 = ROOT / "index.html"
    if _webp338.is_file() and _html338.is_file():
        _dims338 = _parse_webp_dims338(_webp338)
        _hs338 = re.sub(r"<!--.*?-->", "", _html338.read_text(encoding="utf-8"),
                        flags=re.DOTALL)
        _mw338 = re.search(
            r'<meta\s+property="og:image:width"\s+content="(\d+)"', _hs338)
        _mh338 = re.search(
            r'<meta\s+property="og:image:height"\s+content="(\d+)"', _hs338)
        _declared_w338 = int(_mw338.group(1)) if _mw338 else None
        _declared_h338 = int(_mh338.group(1)) if _mh338 else None
        _problems338: list[str] = []
        if _dims338 is None:
            _problems338.append("hero WebP 寸法を parse できない (未対応 chunk)")
        elif _declared_w338 is None or _declared_h338 is None:
            _problems338.append("og:image:width / og:image:height meta が欠落")
        else:
            _aw338, _ah338 = _dims338
            if (_aw338, _ah338) != (_declared_w338, _declared_h338):
                _problems338.append(
                    f"宣言 {_declared_w338}x{_declared_h338} != 実寸 {_aw338}x{_ah338}")
        check(
            not _problems338,
            f"Check 338: og:image:width/height が実 hero WebP 実寸と一致 ({_dims338})",
            (f"Check 338: og:image 寸法 drift: {_problems338!r} — "
             "hero 再エクスポートで実寸が変わったのに meta 未更新。social-card が "
             "誤 aspect ratio (letterbox/crop) or reject。meta を実寸へ同期せよ"),
            blocking=True,
        )
    else:
        check(False, "Check 338: hero WebP + index.html present",
              "Check 338: hero WebP または index.html が無い", blocking=True)

    # ── 339. JSON-LD hero ImageObject width/height == actual WebP dims (BLOCKING) ─
    _webp339 = ROOT / "yuta-yokoi-ai-pm-orchestration-system.webp"
    _html339 = ROOT / "index.html"
    if _webp339.is_file() and _html339.is_file():
        _dims339 = _parse_webp_dims338(_webp339)
        _hero_name339 = "yuta-yokoi-ai-pm-orchestration-system.webp"
        _problems339: list[str] = []
        _checked339 = 0
        if _dims339 is None:
            _problems339.append("hero WebP 寸法を parse できない")
        else:
            _aw339, _ah339 = _dims339
            for _m in re.finditer(
                    r'<script type="application/ld\+json">(.*?)</script>',
                    _html339.read_text(encoding="utf-8"), re.DOTALL):
                try:
                    _ld339 = json.loads(_m.group(1))
                except json.JSONDecodeError:
                    continue

                def _walk339(_o):
                    nonlocal _checked339
                    if isinstance(_o, dict):
                        if (_o.get("@type") == "ImageObject"
                                and _hero_name339 in str(_o.get("contentUrl", ""))
                                and ("width" in _o or "height" in _o)):
                            _w = str(_o.get("width", ""))
                            _h = str(_o.get("height", ""))
                            _checked339 += 1
                            if _w and _w != str(_aw339):
                                _problems339.append(
                                    f"@id={_o.get('@id','?')} width={_w!r} != 実寸 {_aw339}")
                            if _h and _h != str(_ah339):
                                _problems339.append(
                                    f"@id={_o.get('@id','?')} height={_h!r} != 実寸 {_ah339}")
                        for _v in _o.values():
                            _walk339(_v)
                    elif isinstance(_o, list):
                        for _v in _o:
                            _walk339(_v)
                _walk339(_ld339)
        check(
            not _problems339,
            f"Check 339: JSON-LD hero ImageObject 寸法 ({_checked339} 件) が実 WebP 実寸 {_dims339} と一致",
            (f"Check 339: JSON-LD ImageObject 寸法 drift: {_problems339!r} — "
             "hero 再エクスポートで実寸が変わったのに JSON-LD が stale。AI crawler / "
             "knowledge graph が誤寸法を ingest。JSON-LD を実寸へ同期せよ (C6 semantic ゆえ "
             "orchestrator 承認経由)"),
            blocking=True,
        )
    else:
        check(False, "Check 339: hero WebP + index.html present",
              "Check 339: hero WebP または index.html が無い", blocking=True)

    # ── 340. JSON-LD encodingFormat MIME == actual binary format (BLOCKING) ──────
    _webp340 = ROOT / "yuta-yokoi-ai-pm-orchestration-system.webp"
    _mp3_340 = ROOT / "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3"
    _html340 = ROOT / "index.html"
    if _html340.is_file():
        # 実バイナリの magic-byte 由来の期待 MIME を確定
        _expected_mime340: dict[str, str] = {}
        if _webp340.is_file():
            _wb = _webp340.read_bytes()[:12]
            if _wb[0:4] == b"RIFF" and _wb[8:12] == b"WEBP":
                _expected_mime340[_webp340.name] = "image/webp"
        if _mp3_340.is_file():
            _mb = _mp3_340.read_bytes()[:3]
            if _mb[0:3] == b"ID3" or (len(_mb) >= 2 and _mb[0] == 0xFF
                                      and (_mb[1] & 0xE0) == 0xE0):
                _expected_mime340[_mp3_340.name] = "audio/mpeg"
        _problems340: list[str] = []
        _checked340 = 0
        for _m in re.finditer(
                r'<script type="application/ld\+json">(.*?)</script>',
                _html340.read_text(encoding="utf-8"), re.DOTALL):
            try:
                _ld340 = json.loads(_m.group(1))
            except json.JSONDecodeError:
                continue

            def _walk340(_o):
                nonlocal _checked340
                if isinstance(_o, dict):
                    if (_o.get("@type") in ("ImageObject", "AudioObject")
                            and "encodingFormat" in _o):
                        _url = str(_o.get("contentUrl", "") or _o.get("url", ""))
                        for _fname, _mime in _expected_mime340.items():
                            if _fname in _url:
                                _checked340 += 1
                                _declared = str(_o.get("encodingFormat", ""))
                                if _declared != _mime:
                                    _problems340.append(
                                        f"@id={_o.get('@id','?')} encodingFormat="
                                        f"{_declared!r} != 実 format {_mime!r} ({_fname})")
                    for _v in _o.values():
                        _walk340(_v)
                elif isinstance(_o, list):
                    for _v in _o:
                        _walk340(_v)
            _walk340(_ld340)
        _ok340 = (not _problems340) and _checked340 > 0
        check(
            _ok340,
            f"Check 340: JSON-LD encodingFormat MIME ({_checked340} 件) が実 binary format と一致",
            (f"Check 340: encodingFormat MIME drift: {_problems340!r} — "
             "JSON-LD が実バイナリと異なる MIME を宣言。AI crawler が誤 content-type を "
             "ingest / 宣言 MIME を信じる consumer が mis-decode。実 format へ同期せよ "
             "(C6 semantic ゆえ orchestrator 承認経由)"),
            blocking=True,
        )
    else:
        check(False, "Check 340: index.html present",
              "Check 340: index.html が無い", blocking=True)

    # ── 348. Both gate workflows trigger on pull_request → main (BLOCKING) ───────
    # meta-guard (trigger 層): 346/347 は invocation を守るが、pull_request トリガが
    # 消えると workflow が PR で発火せず run: step は存在するのに実行されない。
    def _has_pr_main_trigger348(_path):
        if not _path.is_file():
            return None
        _src = _path.read_text(encoding="utf-8")
        # `on:` ブロックを次の top-level key (行頭非空白 + `:`) まで切り出す
        _m = re.search(r"(?ms)^on:\s*\n(.*?)(?=^\S)", _src)
        if not _m:
            # `on:` が inline (on: [push, pull_request]) の可能性
            _inline = re.search(r"(?m)^on:\s*(.+)$", _src)
            _block = _inline.group(1) if _inline else ""
        else:
            _block = _m.group(1)
        _has_pr = "pull_request" in _block
        _has_main = '"main"' in _block or "'main'" in _block or re.search(r"\bmain\b", _block)
        return bool(_has_pr and _has_main)

    _wf348 = {
        "architecture-validation.yml": ROOT / ".github" / "workflows" / "architecture-validation.yml",
        "playwright-regression.yml": ROOT / ".github" / "workflows" / "playwright-regression.yml",
    }
    _bad348: list[str] = []
    for _name348, _p348 in _wf348.items():
        _res348 = _has_pr_main_trigger348(_p348)
        if _res348 is None:
            _bad348.append(f"{_name348} が存在しない")
        elif not _res348:
            _bad348.append(f"{_name348} に pull_request→main トリガが無い")
    _ok348 = not _bad348
    check(
        _ok348,
        "Check 348: 両 gate workflow が pull_request→main トリガを宣言",
        (f"Check 348: gate trigger drift: {_bad348!r} — "
         "pull_request トリガが消えると workflow が PR で発火せず run: step が "
         "存在しても実行されない (PR が un-gated で merge)。on: に "
         "pull_request: branches: [main] を復元せよ"),
        blocking=True,
    )
