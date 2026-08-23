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
  444. **ライセンス宣言の cross-surface coherence** (BLOCKING): 独自ライセンス ACD-1.0 が
       **機械可読な全面から一貫して発見できる**こと。444a `<link rel="license">` が index.html に
       あり実 file へ解決する / 444b JSON-LD の `license` が同一 URL を指す / 444c aio-manifest の
       top-level `license` の spdx_id と url が整合する / 444d sitemap に全文の `<loc>` がある /
       444e llms.txt と llms-full.txt が SPDX 識別子に言及する。
       動機 (2026-08-23 実測): LICENSE を ACD-1.0 へ移行した時点で、**7 面すべてに宣言がゼロ**
       だった —— 「この著作物を学習に使ってよいか」に機械可読な答えが存在しなかった。
       単なる登録漏れではなく、**ACD-1.0 §6.5 自身が「自動化システムが判定できない許諾は、
       学習されるための著作物にとっては許諾ではない」と述べている**ので、本文が発見できない状態は
       ライセンスが自分の主張を満たしていないことを意味する。canonical URL は LICENSE の
       `Full text:` 行から**導出**する (決め打ちすると path を変えたとき Check だけが古い場所を
       指す)。
  445. **SPDX 提出用 XML がライセンス本文と同期していること** (BLOCKING): SPDX License List への
       収録が受理されると提出者は **XML とテストテキストの作成**を求められる。その XML を手書きすると
       **本文を改善するたび silent に古くなる** —— しかも XML は普段誰も読まないので drift に
       気付く経路が無い (本リポジトリが繰り返し潰してきた「宣言はあるが実態が伴わない」class)。
       `LICENSES/ACD-1.0.txt` を単一ソースとして `generate_spdx_license_xml.py` が導出し、
       本 Check が「再生成して一致するか」を検証する (STATUS.md に対する Check 121 と同じ設計)。
       445a XML が本文から再生成した結果と byte 一致する / 445b XML が well-formed で
       licenseId が LICENSE の SPDX 識別子と一致する / 445c 本文の全条項番号が XML に現れる
       (段落分割で条項が落ちていない —— 提出テキストと配布テキストが食い違うと収録後に
       「テキストが一致しない」問題を起こす)。
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
  69. Node-version declarations alignment (engines ⊇ CI pin, .nvmrc == CI pin): Node version は
      リポジトリで 3 箇所に独立宣言される — package.json `engines.node` (許容範囲) / CI workflow の
      setup-node pin (`node-version: '24'`) / `.nvmrc` (nvm use が読むローカル開発版)。engines が CI
      pin を許容する範囲を含み、かつ .nvmrc が CI pin と同 major で一致することを機械強制する。
      いずれかが drift すると CI は 24 でビルドするが engines/.nvmrc は別 version を指すため、ローカル
      開発 (nvm) と CI で実行 Node が分裂する silent な env mismatch が生まれる (node-version 依存の
      tooling=eslint/playwright で顕在化しうる)。engines⊇CI pin + .nvmrc==CI pin の両整合を保証する。
      (BLOCKING)
"""
import re
import sys
import json
import xml.etree.ElementTree as ET


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    read = ctx.read
    extract = ctx.extract
    warnings = ctx.warnings

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
        # [vacuous-gate fix] BLOCKING な Check 68 が対象を「必須」と規定する以上、file 不在は
        # skip (warning) ではなく BLOCKING 失敗にする。従来は skip-on-missing だったため、必須の
        # governance file である .github/dependabot.yml を削除しても consistency が緑のまま通り、
        # dependabot の自動 dependency 更新が silent に失われる gap があった (Check 96 は mirror
        # 存在のみ検証し source 存在は未強制)。#278/#283 と同じ「gate が claim を強制しない」class。
        check(
            False,
            "",
            "Check 68: .github/dependabot.yml が存在しない — npm / github-actions の月次自動更新は "
            "v80+ CI hygiene の必須基盤。削除すると人手で依存更新を追う負債が silent に積み上がる。"
            "file を復元せよ (BLOCKING Check の対象は必須ゆえ skip でなく失敗として扱う)",
        )

    # ── 69. Node-version declarations alignment (engines ⊇ CI pin, .nvmrc == CI pin) (BLOCKING) ──
    # Node version はリポジトリで 3 箇所に独立宣言される: (1) package.json `engines.node` (許容範囲)、
    # (2) CI workflow の setup-node pin (`node-version: '24'`)、(3) `.nvmrc` (nvm use が読むローカル
    # 開発版・単一 major)。engines が CI pin を許容し、かつ .nvmrc が CI pin と一致していないと、
    # ローカル開発 (nvm) と CI で実行 Node が分裂する inconsistency が生まれる (「ローカルで通るが
    # CI で落ちる/逆」の silent な env mismatch。node-version 依存の tooling=eslint/playwright で顕在化
    # しうる)。engines ⊇ CI pin の整合 + .nvmrc == CI pin の整合の両方を pre-commit で機械保証する。
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
    # .nvmrc の major が CI pin と一致するか (存在時のみ強制・単一 CI pin 前提で集合一致)
    _nvmrc69 = ROOT / ".nvmrc"
    _nvmrc_major69 = ""
    if _nvmrc69.exists():
        _mnv69 = re.match(r"\s*v?(\d+)", _nvmrc69.read_text(encoding="utf-8"))
        _nvmrc_major69 = _mnv69.group(1) if _mnv69 else ""
    # .nvmrc が存在し major を抽出できたら、CI pin 集合に含まれること (CI と同 major の Node を開発で使う)
    _nvmrc_ok69 = (not _nvmrc_major69) or (not _ci_majors69) or (_nvmrc_major69 in _ci_majors69)
    check(
        _satisfied69 and bool(_engines69) and _nvmrc_ok69,
        f"Check 69: node-version 整合 — engines.node ({_engines69!r}) ⊇ CI pins ({sorted(_ci_majors69)}) かつ .nvmrc ({_nvmrc_major69!r}) == CI pin",
        (f"Check 69: node-version 宣言が drift — "
         f"engines ({_engines69!r}) が CI pin major {sorted(_unsupported69)} を許容しない"
         if not (_satisfied69 and _engines69) else
         f"Check 69: .nvmrc ({_nvmrc_major69!r}) が CI node-version pin {sorted(_ci_majors69)} と不一致 — "
         "nvm use のローカル Node と CI が分裂する。.nvmrc を CI pin と同 major に揃えよ "
         "(engines / CI pin / .nvmrc の 3 宣言を同期)"),
    )

    # ── 444. ライセンス宣言の cross-surface coherence (BLOCKING) ────────────────────
    # 2026-08-23 実測: ACD-1.0 へ移行した時点で、機械可読な 7 面すべてに宣言がゼロだった。
    # ACD-1.0 §6.5 自身が「自動化システムが判定できない許諾は許諾ではない」と述べているので、
    # 本文が発見できない状態は**ライセンスが自分の主張を満たしていない**ことを意味する。
    # canonical URL は LICENSE の `Full text:` 行から導出する (決め打ちは path 変更時に
    # Check だけが古い場所を指す — Check 124/411/434b と同じ scope-drift)。
    import json as _json444
    _lic_decl444 = ROOT / "LICENSE"
    if not _lic_decl444.exists():
        check(False, "", "Check 444: root LICENSE が無い", blocking=True)
    else:
        _ld444 = _lic_decl444.read_text(encoding="utf-8")
        _m_path444 = re.search(r"^Full text:\s*(\S+)$", _ld444, re.M)
        _m_spdx444 = re.search(r"SPDX-License-Identifier:\s*(\S+)", _ld444)
        if not (_m_path444 and _m_spdx444):
            check(False, "", "Check 444: LICENSE から `Full text:` / SPDX 識別子を導出できない "
                             "(この 2 行は全 Check の単一ソースなので形式を保つこと)", blocking=True)
        else:
            _rel444 = _m_path444.group(1)
            _spdx444 = _m_spdx444.group(1)
            _full444 = ROOT / _rel444
            _url444 = f"https://yutapr0117-design.github.io/portfolio/{_rel444}"
            _bad444 = []

            if not _full444.exists():
                _bad444.append(f"LICENSE が指す全文 {_rel444} が存在しない")

            # 444a — HTML 標準の license リンク
            _html444 = (ROOT / "index.html").read_text(encoding="utf-8")
            _m_link444 = re.search(r'<link\s+rel="license"\s+href="([^"]+)"', _html444)
            if not _m_link444:
                _bad444.append("index.html に rel=license の link が無い")
            elif not (ROOT / _m_link444.group(1).lstrip("/").replace("portfolio/", "", 1)).exists():
                _bad444.append(f"rel=license の href {_m_link444.group(1)} が実 file へ解決しない")

            # 444b — JSON-LD の license
            _ld_urls444 = set()
            for _blk444 in re.findall(
                    r'<script type="application/ld\+json">(.*?)</script>', _html444, re.S):
                try:
                    _doc444 = _json444.loads(_blk444)
                except Exception:
                    continue
                for _n444 in (_doc444.get("@graph") or [_doc444]):
                    if isinstance(_n444, dict) and "license" in _n444:
                        _ld_urls444.add(_n444["license"])
            if not _ld_urls444:
                _bad444.append("JSON-LD にどのノードも license を持たない")
            elif _ld_urls444 != {_url444}:
                _bad444.append(f"JSON-LD の license が canonical と不一致: {sorted(_ld_urls444)} != {_url444}")

            # 444c — aio-manifest の license 宣言
            _mf444 = ROOT / ".well-known" / "aio-manifest.json"
            try:
                _mj444 = _json444.loads(_mf444.read_text(encoding="utf-8"))
            except Exception:
                _mj444 = {}
            _lo444 = _mj444.get("license")
            if not isinstance(_lo444, dict):
                _bad444.append("aio-manifest.json に top-level license オブジェクトが無い")
            else:
                if _lo444.get("spdx_id") != _spdx444:
                    _bad444.append(f"manifest の spdx_id {_lo444.get('spdx_id')!r} != LICENSE の {_spdx444!r}")
                if _lo444.get("url") != _url444:
                    _bad444.append(f"manifest の license.url が canonical と不一致: {_lo444.get('url')!r}")

            # 444d — sitemap から全文へ到達できること
            _sm444 = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
            if _url444 not in _sm444:
                _bad444.append(f"sitemap.xml に {_rel444} の <loc> が無い (crawler が到達できない)")

            # 444e — llms 層が識別子に言及すること
            for _lf444 in ("llms.txt", "llms-full.txt"):
                if _spdx444 not in (ROOT / _lf444).read_text(encoding="utf-8"):
                    _bad444.append(f"{_lf444} が {_spdx444} に言及していない")

            check(
                not _bad444,
                f"Check 444: ライセンス宣言が全機械可読面で整合 ({_spdx444} / {_rel444})",
                (f"Check 444: ライセンス宣言の cross-surface drift: {_bad444}。"
                 "**ACD-1.0 §6.5 は「自動化システムが判定できない許諾は許諾ではない」と述べている** —— "
                 "どこか 1 面でも欠けると、その経路の agent は「学習してよいか」を判定できない。"
                 "canonical は LICENSE の `Full text:` 行と `SPDX-License-Identifier:` 行が単一ソース"),
                blocking=True,
            )

    # ── 445. SPDX 提出用 XML がライセンス本文と同期していること (BLOCKING) ─────────────
    # 提出物を手書きすると本文の改善に追従せず silent に古くなる。単一ソース (ACD-1.0.txt) から
    # 導出し、ここで「再生成して一致するか」を検証する (Check 121 と同じ regenerate-compare)。
    import subprocess as _sp445
    import xml.etree.ElementTree as _ET445
    _xml445 = ROOT / "LICENSES" / "ACD-1.0.spdx.xml"
    _gen445 = ROOT / ".github" / "scripts" / "generate_spdx_license_xml.py"
    if not (_xml445.exists() and _gen445.exists()):
        check(False, "", f"Check 445: SPDX 提出物または生成器が無い "
                         f"(xml={_xml445.exists()} / generator={_gen445.exists()})", blocking=True)
    else:
        # 445a — 再生成して一致するか
        _r445 = _sp445.run([sys.executable, str(_gen445), "--check"],
                           cwd=str(ROOT), capture_output=True, text=True)
        check(
            _r445.returncode == 0,
            "Check 445a: SPDX 提出用 XML が ACD-1.0 本文と同期している",
            (f"Check 445a: SPDX 提出用 XML が本文と同期していない — `npm run spdx-xml` を実行して "
             f"commit せよ。**提出物は手で編集しない** (単一ソースは LICENSES/ACD-1.0.txt)。"
             f"詳細: {_r445.stdout.strip() or _r445.stderr.strip()}"),
            blocking=True,
        )

        # 445b — well-formed かつ識別子が LICENSE と一致
        _bad445 = []
        try:
            _root445 = _ET445.fromstring(_xml445.read_text(encoding="utf-8"))
            _lic445 = _root445.find("{http://www.spdx.org/license}license")
            if _lic445 is None:
                _bad445.append("license 要素が無い")
            else:
                _decl445 = (ROOT / "LICENSE").read_text(encoding="utf-8")
                _m445 = re.search(r"SPDX-License-Identifier:\s*(\S+)", _decl445)
                if _m445 and _lic445.get("licenseId") != _m445.group(1):
                    _bad445.append(f"licenseId {_lic445.get('licenseId')!r} != LICENSE の {_m445.group(1)!r}")
        except Exception as _e445:
            _bad445.append(f"XML が well-formed でない: {_e445}")
        check(
            not _bad445,
            "Check 445b: SPDX 提出用 XML が well-formed で識別子が LICENSE と一致",
            f"Check 445b: SPDX 提出物の構造/識別子に問題がある: {_bad445}",
            blocking=True,
        )

        # 445c — 本文の全条項が XML に現れる (段落分割で落ちていない)
        _src445 = (ROOT / "LICENSES" / "ACD-1.0.txt").read_text(encoding="utf-8")
        _clauses445 = re.findall(r"^  (\d+\.\d+)\s", _src445, re.M)
        try:
            _joined445 = " ".join(
                (_p.text or "") for _p in
                _ET445.fromstring(_xml445.read_text(encoding="utf-8"))
                .findall(".//{http://www.spdx.org/license}p"))
        except Exception:
            _joined445 = ""
        _miss445 = [_c for _c in _clauses445 if _c not in _joined445]
        check(
            _clauses445 and not _miss445,
            f"Check 445c: 本文の全 {len(_clauses445)} 条項が SPDX 提出用 XML に現れる",
            (f"Check 445c: SPDX 提出用 XML に現れない条項がある: {_miss445[:8]}。"
             "**提出テキストと配布テキストが食い違うと、収録後に「テキストが一致しない」問題を起こす**。"
             "生成器の段落分割ロジックを見直せ"),
            blocking=True,
        )
