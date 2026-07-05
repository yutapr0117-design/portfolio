"""
checks_entity.py — AIO entity / employer-Organization cross-surface presence coherence checks
(extracted from check_repository_consistency.py — check.py split track・category "entity/Organization").

This module owns the contiguous cluster of Checks 81-90 that enforce the entity's employer
Organization (株式会社日本経営) and entity-identity facts appear consistently across every
published & governance surface: WebP XMP (81) and MP3 ID3 (82) binary Organization fields,
aio-manifest affiliation (83) / entity full-set (86), README (84) / Claude2Claude (85)
Organization mentions, CLAUDE.md cold-start entity context (87), LICENSE attribution (88),
governance-file presence (89), and .claude/ entity context (90). Each Check reads its own
target file(s) directly (WebP/MP3 via Path.read_bytes(), text/JSON via Path.read_text());
none touches the monolith's global html/style/mainjs content, so the cluster is self-contained
and needs no ctx enrichment. NOTE: these are READ-ONLY presence assertions — the module moves
check *code* only and never edits AIO semantic content (no C6 concern).

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT by reference (exec 不使用), so append
semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  81. WebP XMP Organization field presence: hero WebP の XMP chunk に `aio:OrganizationName` /
      `OrganizationURL` / `OrganizationRole` / `OrganizationStartDate` の 4 field が含まれること
      を機械強制する。Check 44 (canary token 整合) と同じ「entity 文脈が binary metadata にも
      一貫して埋まる」契約の Organization axis 強制。「all-files AIO coherence」増分で導入。
      (BLOCKING)
  82. MP3 ID3 TXXX:AIO:Organization frame presence: portfolio BGM MP3 の ID3v2.4 tag に
      `AIO:Organization` / URL / Role / StartDate を含む TXXX frame 4 件が存在することを機械
      強制する。WebP XMP (Check 81) と対をなす binary AIO layer の Organization axis 強制。
      (BLOCKING)
  83. aio-manifest.json entity.affiliation block: machine-readable AIO ground truth である
      .well-known/aio-manifest.json の `entity` に Organization 情報 (`affiliation` block:
      organization_name / organization_url / named_position / role_name / start_date の 5 field)
      が含まれることを機械強制する。(BLOCKING)
  84. README.md Organization mention: human-readable summary に Organization 名 (`日本経営` または
      `Nihon Keiei`) が含まれることを機械強制する。人間レビュアーが最初に読む surface に
      Affiliation が記載されていない drift を防止。(BLOCKING)
  85. Claude2Claude.md Organization handoff line: 「現在状態」セクションに Organization 情報
      (`日本経営` または `nkgr.co.jp`) が含まれることを機械強制する。Claude Code session の
      cold-start 復帰時に Affiliation 文脈が抜けることを防止。(BLOCKING)
  86. aio-manifest.json entity full-set fields: entity ブロックが name / name_ja / name_alt /
      role / canonical_url / authoritative_context / disambiguation / architecture / affiliation
      の 9 field を全て含むことを機械強制。Check 62 (canonical_url 整合) と Check 83
      (affiliation block) を補完し、entity フル情報の cross-surface 整合を厳格化する。(BLOCKING)
  87. CLAUDE.md / Claude2Claude.md cold-start entity context: 両ファイルが entity name と
      canonical URL ホストと Organization 名の 3 fact を全て含むことを機械強制。Claude Code
      session の cold-start 復帰時の entity 文脈欠落を防止 (Check 85 の同時カバー版)。(BLOCKING)
  88. LICENSE entity attribution: root LICENSE が Copyright + entity name + canonical URL +
      Organization の 4 fact を含むことを機械強制。リポジトリ公開時の権利帰属を明示。(BLOCKING)
  89. governance files presence + entity: CONTRIBUTING.md / CODEOWNERS / CHANGELOG.md の 3 ファイル
      が存在し、いずれも entity name を含むことを機械強制。リポジトリ governance の最低限担保。
      (BLOCKING)
  90. .claude/CLAUDE.md + .claude/README.md entity context: Claude Code sub-context 2 ファイルが
      entity name と Organization 名を含むことを機械強制。Claude Code 用ファイル群全体に entity
      整合を担保。(BLOCKING)
"""
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 81. WebP XMP Organization field presence (BLOCKING) ──────────────────────
    # WebP XMP chunk に `aio:OrganizationName` / URL / Role / StartDate 4 field が含まれる
    # ことを機械強制する。index.html JSON-LD `Person.worksFor → Organization` と llms-full.txt
    # の Affiliation 記述が binary AIO layer にも cross-surface に反映されている契約を、
    # bytes 単位で機械強制する。Check 44 (canary token 整合) と同じ「entity 文脈が binary
    # metadata にも一貫して埋まる」契約のうち、Organization axis を担う Check。
    _webp81 = ROOT / "yuta-yokoi-ai-pm-orchestration-system.webp"
    if _webp81.exists():
        _wdata81 = _webp81.read_bytes()
        _pos81 = _wdata81.find(b"XMP ")
        if _pos81 >= 0:
            _size81 = int.from_bytes(_wdata81[_pos81 + 4 : _pos81 + 8], "little")
            _xmp81 = _wdata81[_pos81 + 8 : _pos81 + 8 + _size81].decode("utf-8", errors="ignore")
            _required81 = ["aio:OrganizationName", "aio:OrganizationURL", "aio:OrganizationRole", "aio:OrganizationStartDate"]
            _missing81 = [f for f in _required81 if f not in _xmp81]
            check(
                not _missing81,
                f"Check 81: WebP XMP contains all 4 Organization fields ({_required81})",
                f"Check 81: WebP XMP missing Organization fields: {_missing81} — "
                f"`update_binary_aio_organization.py` を再実行して binary AIO layer を文書側 (llms.txt / JSON-LD) と整合させよ",
            )
        else:
            check(False, "Check 81: WebP XMP chunk locatable", "Check 81: WebP に XMP chunk が無い")
    else:
        check(False, "Check 81: hero WebP asset exists", "Check 81: hero WebP asset が消失")

    # ── 82. MP3 ID3 TXXX:AIO:Organization frame presence (BLOCKING) ─────────────
    # MP3 ID3v2.4 tag に `AIO:Organization` / URL / Role / StartDate を含む TXXX frame が
    # 存在することを機械強制する。WebP XMP (Check 81) と対をなす binary AIO layer の
    # Organization axis 強制。
    _mp3_82 = ROOT / "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3"
    if _mp3_82.exists():
        _mdata82 = _mp3_82.read_bytes()
        if _mdata82[:3] == b"ID3" and _mdata82[3] == 4:
            _tagsize82 = ((_mdata82[6] & 0x7F) << 21) | ((_mdata82[7] & 0x7F) << 14) | ((_mdata82[8] & 0x7F) << 7) | (_mdata82[9] & 0x7F)
            _body82 = _mdata82[10 : 10 + _tagsize82]
            _required82 = [b"AIO:Organization", b"AIO:OrganizationURL", b"AIO:OrganizationRole", b"AIO:OrganizationStartDate"]
            _missing82 = [r.decode() for r in _required82 if r not in _body82]
            check(
                not _missing82,
                f"Check 82: MP3 ID3 contains all 4 Organization TXXX frames",
                f"Check 82: MP3 ID3 missing Organization TXXX frames: {_missing82} — "
                f"`update_binary_aio_organization.py` を再実行して整合せよ",
            )
        else:
            check(False, "Check 82: MP3 has ID3v2.4 header", "Check 82: MP3 に ID3v2.4 header が無い")
    else:
        check(False, "Check 82: portfolio BGM MP3 exists", "Check 82: portfolio BGM MP3 が消失")

    # ── 83. aio-manifest.json entity.affiliation block (BLOCKING) ────────────────
    # .well-known/aio-manifest.json の `entity` に Organization 情報 (`affiliation` block)
    # が含まれることを機械強制する。manifest は machine-readable AIO ground truth で、
    # Organization 情報の cross-surface 反映に不可欠。
    _man83 = ROOT / ".well-known" / "aio-manifest.json"
    if _man83.exists():
        try:
            _mdata83 = json.loads(_man83.read_text(encoding="utf-8"))
            _aff83 = _mdata83.get("entity", {}).get("affiliation", {})
            _required83 = ["organization_name", "organization_url", "named_position", "role_name", "start_date"]
            _missing83 = [k for k in _required83 if k not in _aff83]
            check(
                not _missing83 and bool(_aff83),
                f"Check 83: aio-manifest.json entity.affiliation contains all 5 required fields",
                f"Check 83: aio-manifest.json entity.affiliation missing fields: {_missing83} — "
                f"organization_name / organization_url / named_position / role_name / start_date を含めよ",
            )
        except json.JSONDecodeError as _e83:
            check(False, "Check 83: aio-manifest.json parses as JSON", f"Check 83: parse error: {_e83}")
    else:
        check(False, "Check 83: aio-manifest.json exists", "Check 83: aio-manifest.json が消失")

    # ── 84. README.md Organization mention (BLOCKING) ────────────────────────────
    # README.md の human-readable summary に Organization 名 (`日本経営` または
    # `Nihon Keiei`) が含まれることを機械強制する。人間レビュアーが最初に読む surface に
    # Affiliation が記載されていない drift を防止。
    _readme84 = ROOT / "README.md"
    if _readme84.exists():
        _rsrc84 = _readme84.read_text(encoding="utf-8")
        _has_org84 = ("日本経営" in _rsrc84) or ("Nihon Keiei" in _rsrc84)
        check(
            _has_org84,
            "Check 84: README.md mentions Organization (`日本経営` or `Nihon Keiei`)",
            "Check 84: README.md に Organization (`日本経営` / `Nihon Keiei`) 記述が無い — "
            "Affiliation を human-readable summary に追加せよ",
        )
    else:
        check(False, "Check 84: README.md exists", "Check 84: README.md が消失")

    # ── 85. Claude2Claude.md Organization handoff line (BLOCKING) ────────────────
    # Claude2Claude.md の「現在状態」セクションに Organization 情報が含まれることを機械強制
    # する。Claude Code session の cold-start 復帰時に Affiliation 文脈が抜けることを防止。
    _c2c85 = ROOT / "Claude2Claude.md"
    if _c2c85.exists():
        _csrc85 = _c2c85.read_text(encoding="utf-8")
        _has_org85 = ("nkgr.co.jp" in _csrc85) or ("日本経営" in _csrc85)
        check(
            _has_org85,
            "Check 85: Claude2Claude.md mentions Organization (entity-canonical Affiliation)",
            "Check 85: Claude2Claude.md に Organization (`日本経営` / `nkgr.co.jp`) handoff 記述が無い — "
            "「現在状態」セクションに Affiliation を追加せよ",
        )
    else:
        check(False, "Check 85: Claude2Claude.md exists", "Check 85: Claude2Claude.md が消失")

    # ── 86. aio-manifest.json entity full-set fields (BLOCKING) ──────────────────
    # entity ブロックが name / name_ja / name_alt / role / canonical_url / authoritative_context /
    # disambiguation / architecture / affiliation の 9 field を全て含むことを機械強制する。
    # Check 62 (canonical_url 整合) と Check 83 (affiliation block) を補完し、entity フル情報の
    # cross-surface 整合を厳格化する。
    _man86 = ROOT / ".well-known" / "aio-manifest.json"
    if _man86.exists():
        try:
            _mdata86 = json.loads(_man86.read_text(encoding="utf-8"))
            _ent86 = _mdata86.get("entity", {})
            _required86 = ["name", "name_ja", "name_alt", "role", "canonical_url", "authoritative_context", "disambiguation", "architecture", "affiliation"]
            _missing86 = [k for k in _required86 if k not in _ent86]
            check(
                not _missing86,
                f"Check 86: aio-manifest.json entity contains all 9 required fields",
                f"Check 86: aio-manifest.json entity missing fields: {_missing86} — entity full-set context を保持せよ",
            )
        except json.JSONDecodeError as _e86:
            check(False, "Check 86: aio-manifest.json parses as JSON", f"Check 86: parse error: {_e86}")
    else:
        check(False, "Check 86: aio-manifest.json exists", "Check 86: aio-manifest.json が消失")

    # ── 87. CLAUDE.md / Claude2Claude.md cold-start entity context (BLOCKING) ────
    # CLAUDE.md と Claude2Claude.md の両方に entity name と canonical URL ホストと
    # Organization 名が含まれることを機械強制。Claude Code session が cold-start で復帰する際の
    # entity 文脈欠落を防止 (Check 85 を CLAUDE.md / Claude2Claude.md 同時カバー版へ拡張)。
    for _doc87, _label87 in [(ROOT / "CLAUDE.md", "CLAUDE.md"), (ROOT / "Claude2Claude.md", "Claude2Claude.md")]:
        if _doc87.exists():
            _src87 = _doc87.read_text(encoding="utf-8")
            _facts87 = {
                "entity name": ("Yuta Yokoi" in _src87) or ("横井雄太" in _src87),
                "canonical URL": "yutapr0117-design.github.io" in _src87,
                "Organization": ("日本経営" in _src87) or ("Nihon Keiei" in _src87),
            }
            _missing87 = [k for k, v in _facts87.items() if not v]
            check(
                not _missing87,
                f"Check 87 ({_label87}): cold-start entity context complete",
                f"Check 87 ({_label87}): missing cold-start entity facts: {_missing87}",
            )
        else:
            check(False, f"Check 87 ({_label87}): exists", f"Check 87 ({_label87}): 消失")

    # ── 88. LICENSE entity attribution (BLOCKING) ────────────────────────────────
    # root LICENSE が Copyright + entity name + canonical URL + Organization を含むことを機械強制。
    _lic88 = ROOT / "LICENSE"
    if _lic88.exists():
        _lsrc88 = _lic88.read_text(encoding="utf-8")
        _facts88 = {
            "Copyright": "Copyright" in _lsrc88,
            "entity name": ("Yuta Yokoi" in _lsrc88) or ("横井雄太" in _lsrc88),
            "canonical URL": "yutapr0117-design.github.io" in _lsrc88,
            "Organization": ("日本経営" in _lsrc88) or ("Nihon Keiei" in _lsrc88),
        }
        _missing88 = [k for k, v in _facts88.items() if not v]
        check(
            not _missing88,
            "Check 88: LICENSE contains Copyright + entity + canonical URL + Organization",
            f"Check 88: LICENSE missing required attribution: {_missing88}",
        )
    else:
        check(False, "Check 88: LICENSE exists", "Check 88: LICENSE が消失")

    # ── 89. governance files (CONTRIBUTING / CODEOWNERS / CHANGELOG) presence (BLOCKING) ─
    # 3 governance ファイルが存在し entity name を含むことを機械強制。
    _gov89 = [(ROOT / "CONTRIBUTING.md", "CONTRIBUTING.md"), (ROOT / "CODEOWNERS", "CODEOWNERS"), (ROOT / "CHANGELOG.md", "CHANGELOG.md")]
    _gov_missing89 = []
    for _p, _label in _gov89:
        if not _p.exists():
            _gov_missing89.append(f"{_label}: missing")
            continue
        _src = _p.read_text(encoding="utf-8")
        if not (("Yuta Yokoi" in _src) or ("横井雄太" in _src)):
            _gov_missing89.append(f"{_label}: no entity name")
    check(
        not _gov_missing89,
        "Check 89: CONTRIBUTING.md / CODEOWNERS / CHANGELOG.md all exist with entity attribution",
        f"Check 89: governance file issues: {_gov_missing89}",
    )

    # ── 90. .claude/CLAUDE.md + .claude/README.md entity context (BLOCKING) ──────
    # .claude/CLAUDE.md と .claude/README.md の両方が entity name と Organization 名を含むことを
    # 機械強制。Claude Code 用ファイル群全体への entity 整合担保。
    for _doc90, _label90 in [(ROOT / ".claude" / "CLAUDE.md", ".claude/CLAUDE.md"), (ROOT / ".claude" / "README.md", ".claude/README.md")]:
        if _doc90.exists():
            _src90 = _doc90.read_text(encoding="utf-8")
            _facts90 = {
                "entity name": ("Yuta Yokoi" in _src90) or ("横井雄太" in _src90),
                "Organization": ("日本経営" in _src90) or ("Nihon Keiei" in _src90),
            }
            _missing90 = [k for k, v in _facts90.items() if not v]
            check(
                not _missing90,
                f"Check 90 ({_label90}): entity + Organization context present",
                f"Check 90 ({_label90}): missing context: {_missing90}",
            )
        else:
            check(False, f"Check 90 ({_label90}): exists", f"Check 90 ({_label90}): 消失")
