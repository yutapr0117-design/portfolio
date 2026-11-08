"""mutation_samples_archive6.py — rotate 先 (自動生成)。

rotate_mutation_samples.py が受け皿の余裕を実測して選び、埋まったら次を起こす。
**新しい mutation は mutation_samples.py の tail へ足すこと** (ここは退避先)。
"""
from mutation_samples_common import ROOT, CHECK, CURRENT_DRAFT, CURRENT_DRAFT_VER, PREVIOUS_VER, FROZEN_PREVIOUS, APPLIED_ID, APPLIED_DATE, SUBMISSION_TARGET, NEXT_CHECK  # noqa: F401 (entry 内で参照)

MUTATIONS_ARCHIVE6 = [
    {
    "name": "Check 123a: 運用モデルの節の見出しから「現在の運用モデル」を外す —— 直前の行コメントがその語を持つので通っていた",
    "file": ROOT / "js" / "ai-knowhow-page.js",
    "find": "                class: 'card card--accent-left', 'data-accent': 'primary', role: 'region', 'aria-label': '現在の運用モデル：AI自走運用への進化'\n            },\n                h('div', { class: 'card-body flex flex-col gap-3' },\n                    sectionHeader('🔄', '現在の運用モデル — 対話型から AI 自走運用への進化', C.primary),",
    "replace": "                class: 'card card--accent-left', 'data-accent': 'primary', role: 'region', 'aria-label': '運用の記録：AI自走運用への進化'\n            },\n                h('div', { class: 'card-body flex flex-col gap-3' },\n                    sectionHeader('🔄', '運用の記録 — 対話型から AI 自走運用への進化', C.primary),",
},
    {
    "name": "Check 463: 送る文面の法的レビューの段落を HTML コメントに隠す —— 描画されず送られないのに、生の markdown で照合して通っていた",
    "file": ROOT / "LICENSES" / "ACD-1.0.submission.md",
    "find": "**Legal review: none.** No lawyer has drafted or read it.",
    "replace": "<!-- **Legal review: none.** No lawyer has drafted or read it. -->",
},
    {
    "name": "Check 463: 送る文面から「新規か legacy か」の行を消す —— 申請日の 1 枚は要件に持つのに、§B.0 の照合には無かった",
    "file": ROOT / "LICENSES" / "ACD-1.0.submission.md",
    "find": "Legacy or New:                  New License\nDrafted By Lawyer:              No\nApproved or Used by Projects:   One — my own repository",
    "replace": "Drafted By Lawyer:              No\nDrafted By Lawyer:              No\nApproved or Used by Projects:   One — my own repository",
},
    {
    "name": "Check 468: §8.4 から「Section 8.1 alone governs」の alone を落とす —— 付け足した機能に §8.4 が及ぶかの線が消える (468u の目印)",
    "file": CURRENT_DRAFT,
    "find": "remove. Section 8.1 alone governs a feature added to the Work, by",
    "replace": "remove. Section 8.1 governs a feature added to the Work, by",
},
    {
    "name": "Check 444n: REUSE.toml の全 file への宣言を前の版へ戻す —— 2026-09-23〜11-08 に実際にこの状態だった (どの Check も読んでいなかった)",
    "file": ROOT / "REUSE.toml",
    "find": f'SPDX-License-Identifier = "LicenseRef-{APPLIED_ID}"',
    "replace": 'SPDX-License-Identifier = "LicenseRef-ACD-1.0"',
},
    {
    "name": "Check 238: og:image の 2 本目を属性の順序を変えて足す —— 先頭しか読まない Check 153 には見えず、旧 238 は属性順を固定していた",
    "file": ROOT / "index.html",
    "find": '    <meta property="og:image" content="https://yutapr0117-design.github.io/portfolio/yuta-yokoi-ai-pm-orchestration-system.webp" />',
    "replace": ('    <meta property="og:image" content="https://yutapr0117-design.github.io/portfolio/yuta-yokoi-ai-pm-orchestration-system.webp" />'
                '<meta content="https://example.com/other.webp" property="og:image" />'),
},
    {
    "name": "Check 238: ai:canonical の 2 本目を別の URL で足す —— 先頭しか読まない Check 282 には見えない",
    "file": ROOT / "index.html",
    "find": '    <meta name="ai:canonical" content="https://yutapr0117-design.github.io/portfolio/" />',
    "replace": ('    <meta name="ai:canonical" content="https://yutapr0117-design.github.io/portfolio/" />'
                '<meta name="ai:canonical" content="https://example.com/" />'),
},
    {
    "name": "Check 17: SITE_CONFIG の直前のコメントに旧い値を残したまま LAST_UPDATED を進める —— コメント込みの先頭一致で読むと、コメントの値が比べられて通っていた (値は v74 の間は変わらない)",
    "file": ROOT / "main.js",
    "find": "        const SITE_CONFIG = {\n            VERSION:       'v74',\n            LAST_UPDATED:  '2026-05-31',",
    "replace": "        // 旧: LAST_UPDATED:  '2026-05-31', VERSION:       'v74',\n        const SITE_CONFIG = {\n            VERSION:       'v74',\n            LAST_UPDATED:  '2026-06-01',",
},
    {
    "name": "Check 2: SITE_CONFIG の直前のコメントに旧い値を残したまま VERSION を進める —— 同じ形で版数の同期が見えなかった (Check 177 も同じ理由で発火する)",
    "file": ROOT / "main.js",
    "find": "        const SITE_CONFIG = {\n            VERSION:       'v74',",
    "replace": "        // 旧: VERSION:       'v74',\n        const SITE_CONFIG = {\n            VERSION:       'v75',",
},
    {
    "name": "Check 444a: 旧い版を指す rel=license を先頭に足す —— 先頭の 1 本が実 file へ解決するかだけを見ていた頃は通った (1.0 の全文も実在する)",
    "file": ROOT / "index.html",
    "find": f'<link rel="license" href="/portfolio/LICENSES/{APPLIED_ID}.txt" />',
    "replace": f'<link rel="license" href="/portfolio/LICENSES/ACD-1.0.txt" /><link rel="license" href="/portfolio/LICENSES/{APPLIED_ID}.txt" />',
},
    {
    "name": "Check 444c: manifest の SPDX 式だけを前の版へ戻す —— spdx_id と url しか比べず、同じブロックの中で版が 2 つになっても通った",
    "file": ROOT / ".well-known" / "aio-manifest.json",
    "find": f'"conforming_spdx_expression": "LicenseRef-{APPLIED_ID}",',
    "replace": '"conforming_spdx_expression": "LicenseRef-ACD-1.0",',
},
    {
    "name": "Check 444d: robots.txt で全文を Disallow する —— 全文は sitemap の <loc> しか見ておらず、robots を読まなかった",
    "file": ROOT / "robots.txt",
    "find": f"Allow: /portfolio/LICENSES/{APPLIED_ID}.txt\n",
    "replace": f"Disallow: /portfolio/LICENSES/{APPLIED_ID}.txt\n",
},
    {
    "name": "Check 444e: llms-full.txt の宣言の文だけを別の版にする —— 識別子が file のどこかに 1 回あれば通った",
    "file": ROOT / "llms-full.txt",
    "find": f"Dedication {APPLIED_ID.split('-')[1]} ({APPLIED_ID})**",
    "replace": "Dedication 1.0 (ACD-1.0)**",
},
    {
    "name": "Check 444f: route 追従ノードの license を前の版にする —— SITE_CONFIG の定義行が常に満たしたので、ノードの値は見られていなかった",
    "file": ROOT / "main.js",
    "find": f"'license': SITE_BASE + 'LICENSES/{APPLIED_ID}.txt',",
    "replace": "'license': SITE_BASE + 'LICENSES/ACD-1.0.txt',",
},
    {
    "name": "Check 444h: sitemap の唯一の <image:license> を消す —— 0 件のとき else が無く、画像のライセンス宣言が消えても通った",
    "file": ROOT / "sitemap.xml",
    "find": f"<image:license>https://yutapr0117-design.github.io/portfolio/LICENSES/{APPLIED_ID}.txt</image:license>",
    "replace": "",
},
    {
    "name": "Check 451c: manifest の attribution_required の鍵を改名する —— manifest 側が欠けると比較を飛ばし、答えが消えても OK だった",
    "file": ROOT / ".well-known" / "aio-manifest.json",
    "find": '"attribution_required": false,',
    "replace": '"attribution_required_x": false,',
},
    {
    "name": "Check 441b: 草案の Section 11 への参照を存在しない Section 19 にする —— 凍結した 1.0 しか読まず、動く唯一の本文を見ていなかった",
    "file": CURRENT_DRAFT,
    "find": "Nothing in Section 11 reduces what any other Section of this",
    "replace": "Nothing in Section 19 reduces what any other Section of this",
},
    {
    "name": "Check 441c: 草案の定義語を改名して未使用にする —— 定義が残骸になっても、1.0 だけを読む頃は通った",
    "file": CURRENT_DRAFT,
    "find": '  1.2  "Moral Rights" means',
    "replace": '  1.2  "Author Rights" means',
},
    {
    "name": "Check 441g: 草案に組織名を英語の通称で書く —— Nihon Keiei / nkgr の綴りしか見ていなかった",
    "file": CURRENT_DRAFT,
    "find": "and Section 10.5 applies.",
    "replace": "and Japan Management applies.",
},
    {
    "name": "Check 441g: 草案に複数語の置換テキスト <your name> を入れる —— 置換テキストの照合が空白で止まり、§16.1 の例外も正規表現の偶然で通っていた",
    "file": CURRENT_DRAFT,
    "find": "except by the Steward (Section 16.5), and by",
    "replace": "except by <your name> (Section 16.5), and by",
},
    {
    "name": "Check 468: §16.2 の通知の主語「a Dedicator」を落とす —— タグを残しただけの取り込み手まで通知の適用に入る (468u の目印)",
    "file": CURRENT_DRAFT,
    "find": "accompanies the work. A notice a Dedicator places applies this",
    "replace": "accompanies the work. A notice placed applies this",
},
    {
    "name": "Check 496: CHANGELIST の表の見出しから「件数」の列を外す —— 行は 4 セルのままなので、GFM は 4 列目を描かずに捨てる (2026-11-08 まで実際にこの状態だった)",
    # 表は 1.4 の記録に在る。確定の道具が作る次版の CHANGELIST は空で始まるので、草案の版で引くと確定の日に Check 362 が RED になる (2026-11-08 の予行)
    "file": ROOT / "LICENSES" / "ACD-1.4-CHANGELIST.md",
    "find": "| レンズ | やったこと | 結果 | 件数 |",
    "replace": "| レンズ | やったこと | 結果 |",
},
    {
    "name": "Check 472n: register の英語の索引で、B1 を述べる Piana 氏の引用を読みやすく動かす —— register は入口の照合の外だった (2026-11-08 に加えた)",
    "file": ROOT / "LICENSES" / "ACD-OSI-BOTTLENECKS.md",
    "find": '*"OSI requires prior review by a lawyer"*',
    "replace": '*"OSI requires a prior review by a lawyer"*',
},
    {
    "name": "Check 468: §8.5 の「if, and only if」を「if」へ縮める —— controlled の定義が片方向の条件になり、§8 が及ぶ請求項が広がる (468u の目印)",
    "file": CURRENT_DRAFT,
    "find": "Dedicator if, and only if, at the time in question, the Dedicator has",
    "replace": "Dedicator if, at the time in question, the Dedicator has",
},
]
