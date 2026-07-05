"""
checks_aio_derived.py — AIO C6 derived-value & date-sync tooling integrity checks
(extracted from check_repository_consistency.py — check.py split track・category "AIO derived-value").

This module owns the contiguous cluster of Checks 91-95 that guard the C6 derived-value
machinery: binary metadata date freshness (91), the C6 derived-value exception canon presence
(92), aio-manifest last_metadata_update field (93), the update_aio_digests.py /
update_binary_aio_organization.py tool integrity (94), and the _lib_io.py date helpers (95).
Each Check reads its own target file(s) directly (WebP/MP3 via Path.read_bytes(), text/JSON via
Path.read_text()); none depends on the monolith's global html/style/mainjs content, so the
cluster is self-contained and needs no ctx enrichment. NOTE: like checks_entity.py these are
READ-ONLY integrity assertions — the module moves check *code* only and never edits AIO
semantic content or regenerates digests (no C6 concern).

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT by reference (exec 不使用), so append
semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  91. binary metadata date freshness: WebP XMP の `xmp:ModifyDate` / `xmp:MetadataDate`、MP3 ID3 の
      `AIO:MetadataLastModified`、aio-manifest.json の `last_metadata_update` の 4 日付フィールドが
      全て同一日 (YYYY-MM-DD 一致) であることを機械強制。C6 derived-value 例外条項の運用契約 (binary
      の semantic 編集と日付同期更新) を pre-commit で構造保証。手動経路で日付更新を忘れた場合の
      fail-fast。(BLOCKING)
  92. C6 derived-value exception canon presence: CLAUDE.md と AI2AI.md の C6 説明に
      「derived-value auto-update」または「derived value」の文言が含まれることを機械強制。
      A 案 canon 文言の静かな revert を防止。(BLOCKING)
  93. aio-manifest.json last_metadata_update field present: top-level `last_metadata_update` が
      ISO-8601 形式で存在することを機械強制 (8 案・10 案 — Check 91 の central anchor)。(BLOCKING)
  94. B1/B2 tool date-sync responsibility: `update_aio_digests.py` と `update_binary_aio_organization.py`
      が `_lib_io` から `update_webp_xmp_dates` / `update_mp3_metadata_date` を import している
      ことを機械強制。「日付同期を tool が責務として持つ」契約を構造保護。(BLOCKING)
  95. _lib_io.py date helpers: `_lib_io.py` に `now_iso8601` / `update_webp_xmp_dates` /
      `update_mp3_metadata_date` の 3 public helper が存在することを機械強制 (6 案)。(BLOCKING)
"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 91. binary metadata date freshness (BLOCKING) ────────────────────────────
    # (C 案 + 9 案) WebP XMP の xmp:ModifyDate と xmp:MetadataDate、MP3 ID3 の
    # AIO:MetadataLastModified、aio-manifest.json の last_metadata_update が全て
    # 同一日 (YYYY-MM-DD 一致) であることを機械強制する。binary の semantic 編集と
    # 日付フィールドの同期更新を pre-commit で構造的に保証 (C6 derived-value 例外
    # 条項の運用契約)。手動経路で binary を編集して日付を忘れた場合、本 Check が
    # fail で気づく。
    import re as _re91
    _webp91 = ROOT / "yuta-yokoi-ai-pm-orchestration-system.webp"
    _mp3_91 = ROOT / "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3"
    _man91 = ROOT / ".well-known" / "aio-manifest.json"
    _dates91 = {}
    if _webp91.exists():
        import struct as _struct91
        _wdata91 = _webp91.read_bytes()
        _xp91 = _wdata91.find(b"XMP ")
        if _xp91 >= 0:
            _xs91 = _struct91.unpack("<I", _wdata91[_xp91 + 4 : _xp91 + 8])[0]
            _xtext91 = _wdata91[_xp91 + 8 : _xp91 + 8 + _xs91].decode("utf-8", errors="ignore")
            _m_modify = _re91.search(r"<xmp:ModifyDate>(\d{4}-\d{2}-\d{2})", _xtext91)
            _m_metadata = _re91.search(r"<xmp:MetadataDate>(\d{4}-\d{2}-\d{2})", _xtext91)
            if _m_modify: _dates91["webp:ModifyDate"] = _m_modify.group(1)
            if _m_metadata: _dates91["webp:MetadataDate"] = _m_metadata.group(1)
    if _mp3_91.exists():
        _mdata91 = _mp3_91.read_bytes()
        _m_id3 = _re91.search(rb"AIO:MetadataLastModified\x00(\d{4}-\d{2}-\d{2})", _mdata91)
        if _m_id3: _dates91["mp3:AIO:MetadataLastModified"] = _m_id3.group(1).decode("ascii")
    if _man91.exists():
        try:
            _md91 = json.loads(_man91.read_text(encoding="utf-8"))
            _lmu91 = _md91.get("last_metadata_update", "")
            _m_lmu = _re91.match(r"(\d{4}-\d{2}-\d{2})", _lmu91)
            if _m_lmu: _dates91["manifest:last_metadata_update"] = _m_lmu.group(1)
        except json.JSONDecodeError:
            pass
    _unique_dates91 = set(_dates91.values())
    check(
        len(_unique_dates91) == 1 and len(_dates91) >= 4,
        f"Check 91: all {len(_dates91)} binary/manifest date fields share one date ({list(_unique_dates91)[0] if _unique_dates91 else 'none'})",
        f"Check 91: binary/manifest date drift — {_dates91}. C6 derived-value 例外条項に従い、"
        f"`update_binary_aio_organization.py` または `update_aio_digests.py` を再実行して日付を同期せよ",
    )

    # ── 92. C6 derived-value exception canon presence (BLOCKING) ─────────────────
    # (A 案 canon check) CLAUDE.md と AI2AI.md の両方の C6 説明に「derived-value
    # auto-update」「Exception」の文言が含まれることを機械強制する。canon 文言の
    # 静かな revert を防止。
    _c6_canon_files = [(ROOT / "CLAUDE.md", "CLAUDE.md"), (ROOT / "AI2AI.md", "AI2AI.md")]
    _c6_canon_missing = []
    for _p, _label in _c6_canon_files:
        if not _p.exists():
            _c6_canon_missing.append(f"{_label}: missing")
            continue
        _src = _p.read_text(encoding="utf-8")
        if "derived-value auto-update" not in _src and "derived value" not in _src.lower():
            _c6_canon_missing.append(f"{_label}: no derived-value clause")
    check(
        not _c6_canon_missing,
        "Check 92: CLAUDE.md + AI2AI.md C6 both document the derived-value auto-update exception",
        f"Check 92: C6 canon missing derived-value clause: {_c6_canon_missing} — "
        f"canon 文言が静かに revert された可能性。A 案 例外条項を再記述せよ",
    )

    # ── 93. aio-manifest.json last_metadata_update field present (BLOCKING) ──────
    # (8 案 + 10 案) aio-manifest.json に top-level `last_metadata_update` が存在する
    # ことを機械強制 (Check 91 が真値として使う central anchor)。
    _man93 = ROOT / ".well-known" / "aio-manifest.json"
    if _man93.exists():
        try:
            _md93 = json.loads(_man93.read_text(encoding="utf-8"))
            _lmu93 = _md93.get("last_metadata_update", "")
            _ok93 = bool(_lmu93 and _re91.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", _lmu93))
            check(
                _ok93,
                f"Check 93: aio-manifest.json last_metadata_update = {_lmu93} (ISO-8601)",
                f"Check 93: aio-manifest.json last_metadata_update missing or malformed: {_lmu93!r}",
            )
        except json.JSONDecodeError as _e93:
            check(False, "Check 93: aio-manifest.json parses", f"Check 93: parse error: {_e93}")
    else:
        check(False, "Check 93: aio-manifest.json exists", "Check 93: aio-manifest.json missing")

    # ── 94. update_aio_digests.py / update_binary_aio_organization.py tool integrity (BLOCKING) ─
    # (B1 + B2 案) 両 tool が `_lib_io` から helper を import していることを機械強制。
    # 「日付同期を tool が責務として持つ」契約を構造的に保護。
    _tools94 = [
        (ROOT / ".github" / "scripts" / "update_aio_digests.py", "update_aio_digests.py"),
        (ROOT / ".github" / "scripts" / "update_binary_aio_organization.py", "update_binary_aio_organization.py"),
    ]
    _tool_missing94 = []
    for _p, _label in _tools94:
        if not _p.exists():
            _tool_missing94.append(f"{_label}: missing")
            continue
        _src = _p.read_text(encoding="utf-8")
        if "update_webp_xmp_dates" not in _src or "update_mp3_metadata_date" not in _src:
            _tool_missing94.append(f"{_label}: missing date sync responsibility")
    check(
        not _tool_missing94,
        "Check 94: B1/B2 tools (update_aio_digests / update_binary_aio_organization) both reference date sync helpers",
        f"Check 94: tools missing date-sync responsibility: {_tool_missing94}",
    )

    # ── 95. _lib_io.py date helpers (BLOCKING) ───────────────────────────────────
    # (6 案) `_lib_io.py` に `now_iso8601`, `update_webp_xmp_dates`,
    # `update_mp3_metadata_date` の 3 public helper が存在することを機械強制。
    _lib95 = ROOT / ".github" / "scripts" / "_lib_io.py"
    if _lib95.exists():
        _lsrc95 = _lib95.read_text(encoding="utf-8")
        _req95 = ["now_iso8601", "update_webp_xmp_dates", "update_mp3_metadata_date"]
        _missing95 = [fn for fn in _req95 if not _re91.search(rf"^def {fn}\b", _lsrc95, _re91.MULTILINE)]
        check(
            not _missing95,
            f"Check 95: _lib_io.py exports all 3 date helpers ({_req95})",
            f"Check 95: _lib_io.py missing date helpers: {_missing95}",
        )
    else:
        check(False, "Check 95: _lib_io.py exists", "Check 95: _lib_io.py が消失")
