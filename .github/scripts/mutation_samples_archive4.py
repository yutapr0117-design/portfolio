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
    {
    "name": 'Check 91: aio-manifest の last_metadata_update を千年前へずらす —— binary 内の日付と manifest の日付が食い違う (値を含まない prefix で当てる・日付は更新のたび動く)',
    "file": ROOT / ".well-known" / "aio-manifest.json",
    "find": '"last_metadata_update": "2',
    "replace": '"last_metadata_update": "1',
    "check": CHECK,
},
    {
    "name": 'Check 95: _lib_io の日付 helper の定義名を変える —— B1/B2 tool が共有するはずの helper が契約から外れる',
    "file": ROOT / ".github" / "scripts" / "_lib_io.py",
    "find": 'def update_mp3_metadata_date(',
    "replace": 'def update_mp3_metadata_date_v2(',
    "check": CHECK,
},
    {
    "name": "Check 424b: §2 表の 1 行の実測行数の列を数字でない形にする —— 2026-11-01 まで、読めない行は "
            "照合から黙って外れ、外れた 5 行中 4 行が stale のまま Check 424 は OK を出していた (portfolio-bb の発見)",
    "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
    "find": "| `ChatGPT2ChatGPT.md` | ",
    "replace": "| `ChatGPT2ChatGPT.md` | ~",
    "check": CHECK,
},
    {
    "name": 'Check 21: llms の alias 1 つだけ Last-Updated を千年前へ —— alias 間で更新日が食い違う (値を含まない prefix で当てる)',
    "file": ROOT / "llms_well-known.txt",
    "find": '- Last-Updated: 2',
    "replace": '- Last-Updated: 1',
    "check": CHECK,
},
    {
    "name": 'Check 24: llms-full.txt の Last-Updated を千年前へ —— AI2AI.md と 7 日を超えて離れ、v75-v78 の床も割る',
    "file": ROOT / "llms-full.txt",
    # Check 24 は本文の `## Last-Updated` 節を優先して読む (ヘッダ行は fallback)。ヘッダを打つと発火しない
    # (初版で実測) ので、優先して読まれる方を打つ。
    "find": '## Last-Updated\n\n2',
    "replace": '## Last-Updated\n\n1',
    "check": CHECK,
},
    {
    "name": 'Check 27: llms-full.txt の制約範囲の表記を C1–C6 へ戻す —— 範囲の表記だけ古いと、展開する agent は C7 を知らずに動く',
    "file": ROOT / "llms-full.txt",
    "find": 'violates C1–C7',
    "replace": 'violates C1–C6',
    "check": CHECK,
},
    {
    "name": 'Check 31: Claude2Claude.md の現在状態が最新 Session Record 番号を指さなくなる —— 引き継ぎの補助面が canon から遅れる (番号を含まない prefix で当てる)',
    "file": ROOT / "Claude2Claude.md",
    "find": '**最新 Session Record：#',
    "replace": '**最新 Session Record：#X',
    "check": CHECK,
},
    {
    "name": 'Check 32: index.html の JSON-LD を JSON として壊す —— 構造化データが丸ごと読めなくなる',
    "file": ROOT / "index.html",
    "find": '"@context": "https://schema.org",',
    "replace": '"@context": "https://schema.org",,',
    "check": CHECK,
},
    {
    "name": 'Check 38: package.json の name を lockfile と食い違わせる —— npm ci の前提が崩れる',
    "file": ROOT / "package.json",
    "find": '"name": "',
    "replace": '"name": "x-',
    "check": CHECK,
},
    {
    "name": 'Check 44: llms-full.txt の canary token の年をずらす —— 公開面ごとに provenance canary が食い違う',
    "file": ROOT / "llms-full.txt",
    "find": 'SAKURA-AIO-PROVENANCE-CANARY-2026-',
    "replace": 'SAKURA-AIO-PROVENANCE-CANARY-2025-',
    "check": CHECK,
},
    {
    "name": 'Check 104: verify から呼ばれる script の Python 3.10+ ガードを緩める —— 3.9 で走ると構文の違いで途中から黙って壊れる',
    "file": ROOT / ".github" / "scripts" / "check_aio_digests.py",
    "find": 'sys.version_info < (3, 10)',
    "replace": 'sys.version_info < (3, 9)',
    "check": CHECK,
},
    {
    "name": 'Check 105: check-map から Check 480 の行番号を実在しない番号へ —— map と実装の対応が崩れる',
    "file": ROOT / "docs" / "architecture" / "check-repository-consistency-map.md",
    "find": '| 480 | **mutation データ',
    "replace": '| 4800 | **mutation データ',
    "check": CHECK,
},
    {
    "name": 'Check 106: .nvmrc の major を CI の node-version と食い違わせる —— ローカルと CI で別の Node で検証される',
    "file": ROOT / ".nvmrc",
    "find": '24',
    "replace": '22',
    "check": CHECK,
},
    {
    "name": 'Check 116: playwright の reuseExistingServer を true へ —— 手元に残った古い server を掴み、変更前のコードを検証してしまう',
    "file": ROOT / "playwright.config.cjs",
    "find": 'reuseExistingServer: false,',
    "replace": 'reuseExistingServer: true,',
    "check": CHECK,
},
    {
    "name": 'Check 117: screenshot の maxDiffPixelRatio を上限より緩める —— 本物の視覚回帰を見逃す',
    "file": ROOT / "playwright.config.cjs",
    "find": 'maxDiffPixelRatio: 0.02 }',
    "replace": 'maxDiffPixelRatio: 0.5 }',
    "check": CHECK,
},
    {
    "name": 'Check 120: shipped JS+CSS の byte 予算を実測より小さくする —— 予算超過を検出できることの確認',
    "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
    "find": '<!-- PERF-BUDGET-DATA 7',
    "replace": '<!-- PERF-BUDGET-DATA ',
    "check": CHECK,
},
    {
    "name": 'Check 121: STATUS.md の最新 Session Record を手で書き換える —— 機械生成の owner dashboard が実態とずれる',
    "file": ROOT / "STATUS.md",
    "find": '- **最新 Session Record**: #',
    "replace": '- **最新 Session Record**: #X',
    "check": CHECK,
},
    {
    "name": 'Check 6: style.css に古い release marker を戻す —— 版の記述が CSS の中で古いまま残る',
    "file": ROOT / "style.css",
    "find": '/* ╔══',
    "replace": '/* NEXT_PLANNED_RELEASE */\n        /* ╔══',
    "check": CHECK,
},
    {
    "name": 'Check 7: CSP meta を別名にする —— inline suppressor より前に CSP が来る順序の保証が崩れる',
    "file": ROOT / "index.html",
    "find": '<meta http-equiv="Content-Security-Policy"',
    "replace": '<meta http-equiv="X-Content-Security-Policy"',
    "check": CHECK,
},
    {
    "name": 'Check 10: 手で回す道具 (verify_dossier_quotations.py) に構文エラーを入れる —— verify が呼ばない script の破損は Check 10 だけが見る',
    "file": ROOT / ".github" / "scripts" / "verify_dossier_quotations.py",
    "find": 'def norm(text):',
    "replace": 'def norm(text:',
    "check": CHECK,
},
    {
    "name": 'Check 12: README の現在の記述に古い「72回以上」を戻す',
    "file": ROOT / "README.md",
    "find": '# Yuta Yokoi — AI-Driven PM Portfolio',
    "replace": '# Yuta Yokoi — AI-Driven PM Portfolio 72回以上',
    "check": CHECK,
},
    {
    "name": 'Check 28: CSP 違反を見る e2e の題名を変える —— セキュリティ gate が在ることの保証が消える',
    "file": ROOT / "e2e" / "security-proxy.spec.js",
    "find": "test('No Trusted Types or CSP violations in console',",
    "replace": "test('No Trusted Types or CSP violations in the console log',",
    "check": CHECK,
},
    {
    "name": 'Check 53: index.html の modulepreload の href を存在しない file へ —— 先読みが 404 になり、宣言だけが残る',
    "file": ROOT / "index.html",
    "find": '<link rel="modulepreload" href="./js/pure-utils.js" />',
    "replace": '<link rel="modulepreload" href="./js/pure-utils-missing.js" />',
    "check": CHECK,
},
    {
    "name": 'Check 61: factory module の docstring から factory pattern の印を落とす —— file 単体を読んでも抽出の経緯が分からなくなる',
    "file": ROOT / "js" / "ai-page.js",
    "find": 'factory pattern',
    "replace": 'factory-less',
    "check": CHECK,
},
    {
    "name": "Check 57: modulepreload を 1 行消す —— main.js が import する葉の集合と先読みの集合が食い違い、その葉だけ直列に取得される",
    "file": ROOT / "index.html",
    "find": '    <link rel="modulepreload" href="./js/ui-components.js" />\n',
    "replace": "",
    "check": CHECK,
},
    {
    "name": "Check 468m: §16.4 の Steward 例外から「新しい版番号でのみ」の限定を外す —— Steward が同じ識別子で"
            "別本文を出せる形に戻る (2026-11-01 外部レビュー #279)。語数を変えない置換にして 468 の語数 face と分ける",
    "file": CURRENT_DRAFT,
    # 同じ語句が草案冒頭の変更一覧にも引用されている (初版の find は 2 箇所に当たり、先頭 = 変更一覧を
    # 打って §16.4 は無傷だった)。§16.4 の行だけにある直後の "," まで含めて一意にする。
    "find": "no earlier text has borne,",
    "replace": "an earlier text has borne,",
    "check": CHECK,
},
    {
    "name": 'Check 13: README の現在の記述に「70超」を戻す —— 履歴の文脈でない場所に古い数が残る',
    "file": ROOT / "README.md",
    "find": '# Yuta Yokoi — AI-Driven PM Portfolio',
    "replace": '# Yuta Yokoi — AI-Driven PM Portfolio 70超',
    "check": CHECK,
},
    {
    "name": 'Check 58: e2e の ALL_ROUTES から 1 ルートの名前をずらす —— main.js の switch と全ルート訪問 e2e の集合が食い違う',
    "file": ROOT / "e2e" / "security-proxy.spec.js",
    "find": "{ hash: '#/projects',          name: 'projects' }",
    "replace": "{ hash: '#/projects',          name: 'projectz' }",
    "check": CHECK,
},
    {
    "name": 'Check 66: index.html の <title> から entity 名を落とす —— 検索結果と AI の要約で誰のサイトか分からなくなる',
    "file": ROOT / "index.html",
    "find": '<title>AI-Driven PM yuta｜',
    "replace": '<title>AI-Driven PM｜',
    "check": CHECK,
},
    {
    "name": 'Check 67: workflow の top-level permissions を外す —— 既定の広い token 権限で走る',
    "file": ROOT / ".github" / "workflows" / "update-playwright-snapshots.yml",
    "find": '\npermissions:\n',
    "replace": '\npermissionz:\n',
    "check": CHECK,
},
]
