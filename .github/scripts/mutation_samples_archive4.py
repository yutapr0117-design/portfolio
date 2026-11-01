"""mutation_samples_archive4.py — rotate 先 (自動生成)。

rotate_mutation_samples.py が受け皿の余裕を実測して選び、埋まったら次を起こす。
**新しい mutation は mutation_samples.py の tail へ足すこと** (ここは退避先)。
"""
from mutation_samples_common import ROOT, CHECK, CURRENT_DRAFT, CURRENT_DRAFT_VER, PREVIOUS_VER  # noqa: F401 (entry 内で参照)

MUTATIONS_ARCHIVE4 = [
    {
    "name": "Check 413c: runbook §9 が引用する Check 108 の件数だけを古い値へ戻す —— 4 つの数 "
            "(総数 / source / mirror / 行末の合計) は 413/413b が守るが、同じ行の 5 つ目の数である"
            "**引用の中の数**は誰も見ていなかった (実測 2026-09-28: 284 と 636 を同時に主張していた)",
    "file": ROOT / "docs" / "architecture" / "total-check-runbook.md",
    # anchor は件数そのものを含めない（件数は file 追加のたび動き anchor が orphan 化する）。
    # 数字の直前に "9" を差し込んで値を変える＝実測と必ず食い違う。
    "find": "OK メッセージ `all ",
    "replace": "OK メッセージ `all 9",
    "check": CHECK,
},
    {
    "name": "Check 469 (a): Check 460 の face 列挙から (d) を落とす —— 実装は 19 面のまま宣言だけ 18 面になる。"
            "列挙は減る側へ drift するので「増えたか」では検出できない (479 の凍結リストに残っていた)",
    "file": ROOT / ".github" / "scripts" / "checks_license_self_reporting.py",
    "find": "(d) FAQ mirror の件数、",
    "replace": "FAQ mirror の件数、",
    "check": CHECK,
},
    {
    "name": "Check 460: 読み先の FAQ を改名後の名前へずらす —— 改名を mirror と参照まで正しく直すと他の Check は"
            "全部緑になり、2026-11-01 まで本 Check だけが 19 面まるごと warning で skip していた",
    "file": ROOT / ".github" / "scripts" / "checks_license_self_reporting.py",
    "find": '_fq460 = _read460("ACD-1.0.faq.md")',
    "replace": '_fq460 = _read460("ACD-1.0.faq-renamed.md")',
    "check": CHECK,
},
    {
    "name": "Check 363: JS-LEAF-CEILING marker を消す —— 2026-11-01 まで BLOCKING の 1,000 行上限が"
            "warning 1 行を残して exit 0 のまま外れていた (兄弟の ESLINT / PERF marker は既に BLOCKING)",
    "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
    "find": "<!-- JS-LEAF-CEILING 1000 -->",
    "replace": "<!-- JS LEAF CEILING (removed) -->",
    "check": CHECK,
},
    {
    "name": "Check 468k (mirror / 「いまは」の言い回し): 1.1 の mirror に「いまは `ACD-1.3-DRAFT.txt`」を戻す —— "
            "2026-11-01 まで 468k は LICENSES/*.md の「いまの作業場は」しか見ておらず、同じ古さが 3 箇所残っていた",
    "file": ROOT / "docs" / "files" / "LICENSES" / "ACD-1.1.txt.md",
    "find": "以後の作業場は `FROZEN.md` 冒頭が権威。",
    "replace": "いまは `ACD-1.3-DRAFT.txt`。",
    "check": CHECK,
},
    {
    "name": "Check 468l: 草案の 2 行を語を変えずに 1 行へ繋いで 80 桁超にする —— 1.1〜1.3 はこの形で確定し、"
            "凍結で直せなくなった (2026-11-01 実測)",
    "file": CURRENT_DRAFT,
    # 語を足すと 468 の語数申告の face が先に拾い帰属が曖昧になる (初版で実測)。語を変えずに 2 行を
    # 1 行へ繋いで 80 桁を超えさせ、468l だけを狙う。
    "find": "in any medium and in any form,\n       including source code",
    "replace": "in any medium and in any form, including source code",
    "check": CHECK,
},
    {
    "name": "Check 468: 次版草案の題名行を前の版へ戻す (468j) —— 1.2 を複製した 1.3 草案で題名だけが "
            "7 日間 \"Version 1.2\" のまま残った実例 (2026-10-24)。語数は版数で変わらないので他の face は気付かない",
    "file": CURRENT_DRAFT,
    "find": f"                              Version {CURRENT_DRAFT_VER}\n",
    "replace": f"                              Version {PREVIOUS_VER}\n",
    "check": CHECK,
},
    {
    "name": "Check 468: 英語の入口が作業場を前の版の草案のまま名指す (468k) —— 2026-10-29 に 7 箇所が "
            "1.3 草案を指したままだった実例。語数・条数・題名は草案側の性質なので他の face は気付かない",
    "file": ROOT / "LICENSES" / "REVIEWERS.md",
    "find": f"happens in [`{CURRENT_DRAFT.name}`]({CURRENT_DRAFT.name})",
    "replace": f"happens in [`ACD-{PREVIOUS_VER}-DRAFT.txt`](ACD-{PREVIOUS_VER}-DRAFT.txt)",
    "check": CHECK,
},
    {
    "name": 'Check 83: aio-manifest の entity.affiliation から named_position の key を壊す —— 所属の機械可読な正本が欠ける',
    "file": ROOT / ".well-known" / "aio-manifest.json",
    "find": '"named_position": "',
    "replace": '"named_position_x": "',
    "check": CHECK,
},
    {
    "name": 'Check 84: README の所属から組織名を落とす —— 人間向け要約から Organization が消える',
    "file": ROOT / "README.md",
    "find": '株式会社日本経営 (Nihon Keiei / Japan Management Co., Ltd.) — シェア',
    "replace": '株式会社 (Japan Management Co., Ltd.) — シェア',
    "check": CHECK,
},
    {
    "name": 'Check 85: Claude2Claude.md の現在状態から組織名と組織 URL を落とす —— cold-start の引き継ぎから所属が消える',
    "file": ROOT / "Claude2Claude.md",
    "find": '株式会社日本経営 (Nihon Keiei / 日本経営グループ — 国内最大規模級の医業経営コンサルティングファーム), シェアデータベース事業部 主幹（課長格）, 2026-06-11〜. Organization canonical URL: https://nkgr.co.jp/',
    "replace": '株式会社 (Nihon Keiei / グループ — 国内最大規模級の医業経営コンサルティングファーム), シェアデータベース事業部 主幹（課長格）, 2026-06-11〜. Organization canonical URL: https://example.invalid/',
    "check": CHECK,
},
    {
    "name": 'Check 86: aio-manifest の entity から name_alt の key を壊す —— 別表記での同定が機械可読面から消える',
    "file": ROOT / ".well-known" / "aio-manifest.json",
    "find": '"name_alt": [',
    "replace": '"name_alt_x": [',
    "check": CHECK,
},
    {
    "name": 'Check 88: root LICENSE の著作権表示から Copyright を落とす —— 帰属の起点が読めなくなる',
    "file": ROOT / "LICENSE",
    "find": 'the work originated from Copyright (C) 2026',
    "replace": 'the work originated from (C) 2026',
    "check": CHECK,
},
    {
    "name": 'Check 90: .claude/README.md の所属から組織名を落とす —— Claude Code の sub-context から所属が消える',
    "file": ROOT / ".claude" / "README.md",
    "find": '株式会社日本経営 (Nihon Keiei / Japan Management',
    "replace": '株式会社 (Japan Management',
    "check": CHECK,
},
    {
    "name": "Check 463 (463b): 申請日の 1 枚から「法的レビュー」の行見出しを消す —— 委員長が欠落を名指しした当の項目で、"
            "我々の最大の弱点を述べる行なので書き落とす方向の圧力が構造的にある (2026-11-01 まで §B.0 にしか効いていなかった)",
    "file": ROOT / "LICENSES" / "SUBMISSION-MATERIALS.md",
    "find": "| 法的レビュー | **弁護士のレビューは無い**",
    "replace": "| （未記入） | **弁護士のレビューは無い**",
    "check": CHECK,
},
    {
    "name": 'Check 62: llms-full.txt の Canonical URL を別 origin へずらす —— AIO 層ごとに entity の識別子が食い違う',
    "file": ROOT / "llms-full.txt",
    "find": '> **Canonical URL:** https://yutapr0117-design.github.io/portfolio/',
    "replace": '> **Canonical URL:** https://example.com/portfolio/',
    "check": CHECK,
},
    {
    "name": 'Check 63: robots.txt の Sitemap を別 origin へずらす —— crawler の発見経路が entity の origin と一致しなくなる',
    "file": ROOT / "robots.txt",
    "find": 'Sitemap: https://yutapr0117-design.github.io/portfolio/sitemap.xml',
    "replace": 'Sitemap: https://example.com/portfolio/sitemap.xml',
    "check": CHECK,
},
    {
    "name": 'Check 64: check-map の Check 番号を重複させる —— 同じ番号の行が 2 つあると、どちらの説明が正か読めなくなる',
    "file": ROOT / "docs" / "architecture" / "check-repository-consistency-map.md",
    "find": '| 105 | check-repository-consistency-map.md',
    "replace": '| 104 | check-repository-consistency-map.md',
    "check": CHECK,
},
    {
    "name": 'Check 65: docs/architecture の Last-Updated を ISO-8601 でない書式にする —— 機械が日付を比較できなくなる',
    "file": ROOT / "docs" / "architecture" / "main-js-extraction-map.md",
    "find": 'Last-Updated  : 2026-06-12',
    "replace": 'Last-Updated  : 12 June 2026',
    "check": CHECK,
},
    {
    "name": "Check 480: archive の 1 entry に同じ key をもう 1 つ持たせる —— 衝突解消で 2 entry が融合した形。"
            "重複 key は黙って後勝ちで上書きされ、片方の mutation が消える (2026-11-01 実測)。"
            "対象は hot log ではなく archive (自分自身の entry を打つ self-reference trap を避ける)",
    "file": ROOT / ".github" / "scripts" / "mutation_samples_archive.py",
    "find": '"name": "Check 129 (topbar double-fire): add a direct menuBtn click listener in main.js",',
    "replace": '"name": "Check 129 (topbar double-fire): add a direct menuBtn click listener in main.js",\n        "name": "Check 129 (topbar double-fire): add a direct menuBtn click listener in main.js",',
    "check": CHECK,
},
    {
    "name": 'Check 93: aio-manifest の top-level last_metadata_update の key を壊す —— binary metadata の最終更新が機械可読面から消える',
    "file": ROOT / ".well-known" / "aio-manifest.json",
    "find": '"last_metadata_update": "',
    "replace": '"last_metadata_update_x": "',
    "check": CHECK,
},
    {
    "name": 'Check 94: B2 tool から MP3 の日付同期の呼び出しを外す —— Organization を書き換えても MP3 の日付が進まず、C6 の派生値が semantic 編集に追従しなくなる',
    "file": ROOT / ".github" / "scripts" / "update_binary_aio_organization.py",
    "find": '    from _lib_io import update_webp_xmp_dates, update_mp3_metadata_date\n\n    if update_webp_xmp_dates(WEBP, iso_now):\n        print(f"WebP XMP dates updated to {iso_now}")\n    else:\n        print("WebP XMP dates already current")\n    if update_mp3_metadata_date(MP3, iso_now):',
    "replace": '    from _lib_io import update_webp_xmp_dates\n\n    if update_webp_xmp_dates(WEBP, iso_now):\n        print(f"WebP XMP dates updated to {iso_now}")\n    else:\n        print("WebP XMP dates already current")\n    if False:',
    "check": CHECK,
},
    {
    "name": 'Check 97: 1 対 1 doc の frontmatter から audience を落とす —— 誰向けの doc かが機械で読めなくなる',
    "file": ROOT / "docs" / "files" / "robots.txt.md",
    "find": '\naudience: ',
    "replace": '\naudiences: ',
    "check": CHECK,
},
    {
    "name": 'Check 98: 1 対 1 doc から Change impact の節を落とす —— 変更の波及が書かれない doc が混ざる',
    "file": ROOT / "docs" / "files" / "robots.txt.md",
    "find": '\n## Change impact',
    "replace": '\n## Impact',
    "check": CHECK,
},
]
