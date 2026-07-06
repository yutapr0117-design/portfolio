"""
checks_aio_config.py — AIO entity/crawler identity + CI/config governance checks
(extracted from check_repository_consistency.py — check.py split track・category "AIO/CI config").

Contiguous cluster of Checks 62-69: AIO entity canonical_url cross-surface identity (62), crawler
discovery origin alignment (63), check-map Check-number uniqueness (64), doc Last-Updated ISO-8601
(65), index.html <title> entity-identifier (66), GitHub Actions explicit permissions (67),
dependabot dual-ecosystem (68), package.json engines.node ↔ CI node pin (69). Each Check reads its
own target files directly; no global-content or cross-section var coupling. NOTE: Check 72 (ESLint
baseline absolute-ceiling) is NOT included — it consumes `_bsrc59`/`_budget59` from Check 59, a
separate ESLint-baseline pair (59+72) left in the monolith. Check 70/71 are self-integrity /
already-extracted.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/read/extract by reference (exec 不使用).

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  62. AIO entity canonical_url cross-surface identity: aio-manifest.json の `entity.canonical_url`
      と llms-full.txt の `Canonical URL:` 値が 1 バイトも違わずに一致することを機械強制する。
      Entity の canonical URL は AIO 識別子の最重要 anchor — manifest と canon (llms-full) の
      双方が同じ URL を主張していないと、引用先 / クローラの ground-truth が分かれ、entity
      disambiguation が崩れる。C6 範疇内で「両者が drift したら BLOCKING」する Check 4 (llms 系
      byte-identity) の発想を entity-URL 単位に降ろした検査。(BLOCKING)
  63. Crawler discovery origin alignment: robots.txt `Sitemap:` URL の origin、aio-manifest.json
      `entity.canonical_url` の origin、sitemap.xml の全 `<loc>` の origin が完全に同一である
      ことを機械強制する。クローラは robots.txt → sitemap.xml の順に discover するため、両者
      が origin drift していると crawler は別ホストの URL を「同サイトの一部」と誤認するか
      丸ごと取りこぼす。さらに entity.canonical_url の origin もこれらと一致していないと、AIO
      引用先が外部ホストを指す事態になる。Check 35 (robots.txt の Sitemap directive 存在確認)
      と Check 39 (sitemap loc 実在確認) を補完する「同一 origin 一致」の structural integrity
      検査。(BLOCKING)
  64. check-repository-consistency-map.md Check-number uniqueness: 当該文書の機能カテゴリ別
      (A〜F) 表に列挙された Check 番号がカテゴリをまたいで重複しないことを機械強制する。番号
      重複は「Check N は何の検査か」を一意解決不能にし、新規 Check の挿入位置を誤って番号
      衝突を引き起こす (Stage 5-l / 5-k' の naming 衝突と同種 class)。番号順序自体はカテゴリ
      境界でリセットするため強制しない (各カテゴリ内では ascending、カテゴリ間では非単調) —
      番号一意性のみが本質的に守るべき invariant。(BLOCKING)
  65. doc Last-Updated ISO-8601 format: docs/architecture/*.md の `Last-Updated:` と
      docs/files/*.md mirror の `last-updated:` (YAML frontmatter) について、日付フィールドが
      存在する場合は値が ISO-8601 `YYYY-MM-DD` 形式に厳密に従うことを機械強制する。Last-Updated
      は「文書がいつ真値だったか」を読み手 (AI/human) に伝える正本シグナルで、フォーマット揺れ
      (e.g. `06-13-2026`) は honest-dating 原則を内部から侵食する。Check 34 が sitemap lastmod
      との一致を ADVISORY で見るのに対し、本 Check は「日付フォーマットそのもの」を BLOCKING で
      固定する責務分離。Check 97 が mirror の date presence を見るのに対し本 Check が format を
      担い、honest-dating の scope を 143 ミラー全面へ拡張する。(BLOCKING)
  66. index.html <title> entity-identifier presence: index.html の `<title>` 要素に entity
      primary identifier (`yuta` または `横井`、いずれも case-insensitive) が含まれることを
      機械強制する。`<title>` は SEO/AIO 検索結果の最重要 anchor で、entity 名が含まれていな
      いと SERP/LLM 引用時に「これは誰のサイトか」が一瞬で判定できなくなり、AIO 戦略（「機械
      可読な authority building」）の効果が消失する。C6 範疇内で title の「ブランディング
      anchor」性を機械強制する。(BLOCKING)
  67. GitHub Actions workflow explicit permissions: .github/workflows/*.yml の全ファイルに
      top-level `permissions:` ブロックが明示宣言されていることを機械強制する。permissions: が
      無いと GitHub の default token は full read/write 相当の広い権限になり、CWE-275
      (Missing Actions Permissions) クラスのセキュリティ問題となる。Check 48 (snapshot
      workflow の permissions 二重宣言整合) を補完する「全 workflow 適用版」の security
      baseline。(BLOCKING)
  68. dependabot.yml dual-ecosystem coverage: .github/dependabot.yml が `npm` (devDependencies
      の月次更新) と `github-actions` (workflow action major tag の月次更新) の両 ecosystem を
      update 対象に含むことを機械強制する。Dev tooling と GitHub Actions の自動更新は v80+ CI
      hygiene の基盤で、どちらかが欠落すると人手で月次更新を追跡する負債が積み上がる。設定
      ファイル drift を BLOCKING で防ぐ。(BLOCKING)
  69. package.json engines.node ↔ CI node-version pin alignment: package.json `engines.node`
      が CI workflow の Node version pin (`node-version: '24'`) を許容する範囲を含むことを機械
      強制する。両者が drift していると CI は 24 でビルドするが package.json は別 version を
      強制するため、ローカル開発と CI で実行 Node が分かれる inconsistency が生まれる。
      setup-node@v6 の pin と engines が許容範囲で揃っていることを pre-commit で保証する。
      (BLOCKING)
"""
import re
import json
import xml.etree.ElementTree as ET


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    read = ctx.read
    extract = ctx.extract

    # ── 62. AIO entity canonical_url cross-surface identity (BLOCKING) ────────────
    # aio-manifest.json の `entity.canonical_url` と llms-full.txt の `Canonical URL:` 値が
    # 1 バイトも違わずに一致することを機械強制する。Entity の canonical URL は AIO 識別子の
    # 最重要 anchor — manifest と canon (llms-full) の双方が同じ URL を主張していないと、
    # 引用先 / クローラの ground-truth が分かれ、entity disambiguation が崩れる。C6 の
    # 範疇内で「両者が drift していたら BLOCKING」する。これは Check 4 (llms 系 byte-identity)
    # の発想を entity-URL 単位に降ろした検査。
    _manifest62 = ROOT / ".well-known" / "aio-manifest.json"
    _llmsfull62 = ROOT / "llms-full.txt"
    if _manifest62.exists() and _llmsfull62.exists():
        try:
            _mdata62 = json.loads(_manifest62.read_text(encoding="utf-8"))
            _entity_url62 = _mdata62.get("entity", {}).get("canonical_url", "")
        except json.JSONDecodeError:
            _entity_url62 = ""
        _llms_match62 = re.search(r"Canonical URL:\s*\**\s*(https?://\S+?)\s*(?:\s|\*|$)", _llmsfull62.read_text(encoding="utf-8"))
        _llms_url62 = _llms_match62.group(1) if _llms_match62 else ""
        check(
            _entity_url62 and _entity_url62 == _llms_url62,
            f"Check 62: aio-manifest entity.canonical_url ({_entity_url62}) == llms-full.txt Canonical URL — entity identifier consistent across AIO layers",
            f"Check 62: AIO entity canonical_url drift — aio-manifest={_entity_url62!r}, llms-full={_llms_url62!r}. "
            f"Entity の canonical URL は最重要 anchor。両者を再同期せよ (C6 範疇)",
        )
    else:
        warnings.append("Check 62: aio-manifest.json or llms-full.txt not found — entity-URL check skipped")

    # ── 63. Crawler discovery origin alignment (BLOCKING) ─────────────────────────
    # robots.txt の `Sitemap:` URL の origin、aio-manifest.json `entity.canonical_url` の origin、
    # sitemap.xml の全 `<loc>` の origin が完全に同一であることを機械強制する。クローラは
    # robots.txt → sitemap.xml の順に discover するため、両者が origin drift していると
    # crawler は別ホストの URL を「同サイトの一部」と誤認するか、丸ごと取りこぼす。さらに
    # entity.canonical_url の origin もこれらと一致していないと、AIO 引用先が外部ホストを
    # 指す事態になる。Check 35 (robots.txt の Sitemap directive 存在確認) と Check 39
    # (sitemap loc の実在確認) を補完する「同一 origin 一致」の structural integrity 検査。
    _robots63 = ROOT / "robots.txt"
    _sitemap63 = ROOT / "sitemap.xml"
    if _robots63.exists() and _sitemap63.exists() and _manifest62.exists():
        _sm_match63 = re.search(r"^Sitemap:\s*(https?://\S+)", _robots63.read_text(encoding="utf-8"), re.MULTILINE)
        _sm_url63 = _sm_match63.group(1) if _sm_match63 else ""
        _sm_origin63 = re.match(r"(https?://[^/]+)", _sm_url63)
        _sm_origin_v63 = _sm_origin63.group(1) if _sm_origin63 else ""
        try:
            _tree63 = ET.parse(str(_sitemap63))
            _ns63 = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            _locs63 = [el.text for el in _tree63.getroot().findall(".//s:loc", _ns63) if el.text]
        except ET.ParseError:
            _locs63 = []
        _loc_origins63 = set()
        for _loc in _locs63:
            _m = re.match(r"(https?://[^/]+)", _loc)
            if _m:
                _loc_origins63.add(_m.group(1))
        _entity_origin63 = ""
        _em = re.match(r"(https?://[^/]+)", _entity_url62 or "")
        if _em:
            _entity_origin63 = _em.group(1)
        _all_origins63 = _loc_origins63 | ({_sm_origin_v63} if _sm_origin_v63 else set()) | ({_entity_origin63} if _entity_origin63 else set())
        check(
            len(_all_origins63) == 1,
            f"Check 63: crawler discovery origins all agree at {sorted(_all_origins63)[0] if _all_origins63 else '(none)'} (robots Sitemap + sitemap loc + aio-manifest entity)",
            f"Check 63: crawler discovery origin drift — distinct origins = {sorted(_all_origins63)}. "
            f"robots.txt Sitemap, sitemap.xml <loc> origins, aio-manifest entity.canonical_url origin は全て同一ホストでなければクローラが取りこぼす",
        )
    else:
        warnings.append("Check 63: robots.txt / sitemap.xml / aio-manifest.json 一部欠落 — origin alignment skipped")

    # ── 64. check-repository-consistency-map.md Check-number uniqueness (BLOCKING) ─
    # docs/architecture/check-repository-consistency-map.md は本ファイル check_repository_
    # consistency.py の Check 一覧を機能カテゴリ別 (A〜F) の表形式で列挙したガバナンス文書。
    # 各カテゴリ表は `| N | 検査内容 | BLOCKING |` 形式 (N = Check 番号) で並ぶ。番号がカテ
    # ゴリをまたいで重複すると、人間レビュアーが「Check N は何の検査か」を一意に解決できなく
    # なり、新規 Check の挿入位置を誤って番号衝突を引き起こす (Stage 5-l / 5-k' の naming 衝突
    # と同種の class)。本 Check は全カテゴリ表の Check 番号を抽出し、重複が 0 件であることを
    # 機械強制する。番号順序自体はカテゴリ境界でリセットするため強制しない (各カテゴリ内では
    # ascending だが、カテゴリ間では非単調) — 番号一意性のみが本質的に守るべき invariant。
    _map64 = ROOT / "docs" / "architecture" / "check-repository-consistency-map.md"
    if _map64.exists():
        _msrc64 = _map64.read_text(encoding="utf-8")
        # 行頭が `| <数字><suffix?> |` 形式の行を抽出 (category 表のみ; §3 級別表は行頭 `| BLOCKING` で除外)
        # alpha suffix を含めた identifier として保存 (Check 7 / 7b / 7c は別 identifier として一意性検査)
        _ids64 = re.findall(r"^\|\s*(\d+[a-z]?)\s*\|", _msrc64, re.MULTILINE)
        _seen64: dict[str, int] = {}
        for _id in _ids64:
            _seen64[_id] = _seen64.get(_id, 0) + 1
        _dups64 = sorted([i for i, c in _seen64.items() if c > 1])
        check(
            not _dups64 and len(_ids64) > 0,
            f"Check 64: check-repository-consistency-map.md Check 番号 (alpha suffix 含む) は全カテゴリで一意 "
            f"({len(_ids64)} 行, distinct={len(_seen64)})",
            f"Check 64: check-repository-consistency-map.md に重複した Check 番号: {_dups64} — "
            f"新規 Check の挿入位置を誤って番号衝突 (Stage 5-l / 5-k' クラス)。重複番号を解消せよ",
        )
    else:
        warnings.append("Check 64: check-repository-consistency-map.md not found — uniqueness check skipped")

    # ── 65. doc Last-Updated ISO-8601 format (BLOCKING) ───────────────────────────
    # docs/architecture/ 配下の全 .md (`Last-Updated:`) と docs/files/ 配下の全 mirror
    # (`last-updated:` YAML frontmatter) について、日付フィールドが存在する場合は ISO-8601 の
    # `YYYY-MM-DD` 形式に厳密に従うことを機械強制する。Last-Updated は「文書がいつ真値だったか」を
    # 読み手 (AI/human) に伝える正本シグナルであり、フォーマット揺れ (e.g. `06-13-2026` /
    # `2026.6.13`) は honest-dating 原則（Check 34/AI2AI.md カノン）を内部から侵食する。Check 34 が
    # sitemap lastmod との一致を ADVISORY で見るのに対し、本 Check は「日付フォーマットそのもの」を
    # BLOCKING で固定する責務分離。docs/files mirror (143 件) は Check 97 が presence を見るが
    # フォーマットは未検証だったため、honest-dating の scope をミラー全面へ拡張する。
    _isodate65 = re.compile(r"^\s*Last-Updated\s*:\s*(.+?)\s*$", re.MULTILINE)
    _isodate65_lc = re.compile(r"^\s*last-updated\s*:\s*(.+?)\s*$", re.MULTILINE)
    _isoformat65 = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    _bad_dates65 = []
    for _md65 in sorted((ROOT / "docs" / "architecture").glob("*.md")):
        _src65 = _md65.read_text(encoding="utf-8")
        _m65 = _isodate65.search(_src65)
        if _m65 and not _isoformat65.match(_m65.group(1).strip()):
            _bad_dates65.append(f"{_md65.relative_to(ROOT)}: {_m65.group(1).strip()!r}")
    _docsfiles65 = ROOT / "docs" / "files"
    if _docsfiles65.is_dir():
        for _mir65 in sorted(_docsfiles65.rglob("*.md")):
            if _mir65.name in ("README.md", "_template.md"):
                continue
            _fm65 = re.match(r"^---\s*\n([\s\S]*?)\n---", _mir65.read_text(encoding="utf-8"))
            if not _fm65:
                continue
            _lm65 = _isodate65_lc.search(_fm65.group(1))
            if _lm65 and not _isoformat65.match(_lm65.group(1).strip()):
                _bad_dates65.append(f"{_mir65.relative_to(ROOT)}: {_lm65.group(1).strip()!r}")
    check(
        not _bad_dates65,
        "Check 65: all docs/architecture/*.md Last-Updated + docs/files/*.md last-updated values are ISO-8601 (YYYY-MM-DD)",
        f"Check 65: non-ISO-8601 date values: {_bad_dates65} — "
        f"全 doc の Last-Updated / last-updated は `YYYY-MM-DD` 形式に統一せよ (honest-dating 原則)",
    )

    # ── 66. index.html <title> entity-identifier presence (BLOCKING) ──────────────
    # index.html の `<title>` 要素に entity primary identifier (`yuta` または `横井`、いずれも
    # case-insensitive) が含まれることを機械強制する。`<title>` は SEO/AIO 検索結果の最重要
    # anchor で、entity 名が含まれていないと SERP/LLM 引用時に「これは誰のサイトか」が一瞬で
    # 判定できなくなり、AIO 戦略（「機械可読な authority building」）の効果が消失する。
    # C6 範疇内で title の「ブランディング anchor」性を機械強制する検査。
    _title66 = re.search(r"<title>([^<]+)</title>", read("index.html"), re.IGNORECASE)
    _title_text66 = _title66.group(1) if _title66 else ""
    _has_entity66 = bool(re.search(r"yuta", _title_text66, re.IGNORECASE) or "横井" in _title_text66)
    check(
        _has_entity66,
        f"Check 66: index.html <title> contains entity primary identifier — title={_title_text66!r}",
        f"Check 66: index.html <title> ({_title_text66!r}) lacks entity primary identifier "
        f"('yuta' [case-insensitive] or '横井'). AIO/SEO の entity anchor 強度が失われる。"
        f"title に entity 名を含めて再同期せよ",
    )

    # ── 67. GitHub Actions workflow explicit permissions (BLOCKING) ───────────────
    # .github/workflows/*.yml の全ファイルに top-level `permissions:` ブロックが明示宣言されて
    # いることを機械強制する。permissions: が無いと GitHub の default token は full read/write
    # 相当の広い権限になり、CWE-275 (Missing Actions Permissions) クラスのセキュリティ問題と
    # なる。実運用 5 workflow は既に明示宣言済みだが、新規 workflow 追加時にこれを忘れる drift
    # を pre-commit で構造的に閉じる。Check 48 (snapshot workflow の permissions 二重宣言整合)
    # を補完する「全 workflow 適用版」の security baseline。
    _perm_missing67 = []
    for _wf67 in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
        _wsrc67 = _wf67.read_text(encoding="utf-8")
        if not re.search(r"^permissions:\s*$", _wsrc67, re.MULTILINE):
            _perm_missing67.append(_wf67.name)
    check(
        not _perm_missing67,
        f"Check 67: all {len(list((ROOT / '.github' / 'workflows').glob('*.yml')))} workflows declare an explicit top-level permissions: block",
        f"Check 67: workflows missing top-level permissions: block: {_perm_missing67}. "
        f"GitHub Actions の default token は full r/w — 明示宣言で CWE-275 を防ぐ",
    )

    # ── 68. dependabot.yml dual-ecosystem coverage (BLOCKING) ─────────────────────
    # .github/dependabot.yml が `npm` (devDependencies の月次更新) と `github-actions`
    # (workflow action major tag の月次更新) の両 ecosystem を update 対象に含むことを
    # 機械強制する。Dev tooling (eslint / stylelint / playwright / http-server) と GitHub
    # Actions の自動更新は v80+ CI hygiene の基盤で、どちらかが欠落すると人手で月次更新を
    # 追跡する負債が積み上がる。設定ファイルの drift (e.g. 1 ecosystem だけ残してもう片方を
    # 消す) を BLOCKING で防ぐ。
    _dependabot68 = ROOT / ".github" / "dependabot.yml"
    if _dependabot68.exists():
        _dsrc68 = _dependabot68.read_text(encoding="utf-8")
        _has_npm68 = 'package-ecosystem: "npm"' in _dsrc68 or "package-ecosystem: 'npm'" in _dsrc68
        _has_gha68 = 'package-ecosystem: "github-actions"' in _dsrc68 or "package-ecosystem: 'github-actions'" in _dsrc68
        check(
            _has_npm68 and _has_gha68,
            "Check 68: dependabot.yml covers both npm and github-actions ecosystems",
            f"Check 68: dependabot.yml is missing ecosystem coverage — npm={_has_npm68}, github-actions={_has_gha68}. "
            f"両 ecosystem の月次更新は v80+ CI hygiene の基盤。両方を保持せよ",
        )
    else:
        warnings.append("Check 68: .github/dependabot.yml not found — ecosystem coverage check skipped")

    # ── 69. package.json engines.node ↔ CI node-version pin alignment (BLOCKING) ──
    # package.json `engines.node` が CI workflow の Node version pin (`node-version: '24'`) を
    # 許容する範囲を含むことを機械強制する。両者が drift していると CI は 24 でビルドするが
    # package.json は別 version を強制するため、ローカル開発と CI で実行 Node が分かれる
    # inconsistency が生まれる。setup-node@v6 の pin と engines が許容範囲で揃っていることを
    # pre-commit で保証する。
    _pkg69 = ROOT / "package.json"
    _engines69 = ""
    _ci_nodes69 = []
    if _pkg69.exists():
        try:
            _pkgdata69 = json.loads(_pkg69.read_text(encoding="utf-8"))
            _engines69 = _pkgdata69.get("engines", {}).get("node", "")
        except json.JSONDecodeError:
            _engines69 = ""
    for _wf69 in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
        for _m in re.finditer(r"node-version:\s*['\"]?(\d+)['\"]?", _wf69.read_text(encoding="utf-8")):
            _ci_nodes69.append(_m.group(1))
    # engines が `>=24` または `>=20` などの major-range 表現を含むか、CI pin の major を許容するか
    _ci_majors69 = set(_ci_nodes69)
    _satisfied69 = True
    _unsupported69 = []
    for _maj in _ci_majors69:
        # engines 文字列に当該 major が含まれているか (e.g. ">=24" or "^24" or "24" )
        if not re.search(rf"(>=|\^|~|\b){_maj}(\b|\.)", _engines69):
            _satisfied69 = False
            _unsupported69.append(_maj)
    check(
        _satisfied69 and _engines69,
        f"Check 69: package.json engines.node ({_engines69!r}) covers all CI node-version pins ({sorted(_ci_majors69)})",
        f"Check 69: package.json engines.node ({_engines69!r}) does NOT cover CI node-version pin major(s) {sorted(_unsupported69)}. "
        f"setup-node@v6 の pin と engines が許容範囲で揃っていないとローカル開発と CI が分裂する",
    )
