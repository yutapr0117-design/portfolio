"""mutation_samples_archive7.py — rotate 先 (自動生成)。

rotate_mutation_samples.py が受け皿の余裕を実測して選び、埋まったら次を起こす。
**新しい mutation は mutation_samples.py の tail へ足すこと** (ここは退避先)。
"""
from mutation_samples_common import ROOT, CHECK, CURRENT_DRAFT, CURRENT_DRAFT_VER, PREVIOUS_VER, FROZEN_PREVIOUS, APPLIED_ID, APPLIED_DATE, SUBMISSION_TARGET, NEXT_CHECK  # noqa: F401 (entry 内で参照)

MUTATIONS_ARCHIVE7 = [
    {
    "name": "Check 460: READY-TO-SUBMIT の散文に §B.0 の語数を裸で書き、日付は次の行の別の文にだけ在る —— 表の外は ±3 行の窓で日付を探し、隣の行の「2026-09-07 に同じ理由で書き換えた」を語数の日付と読んでいた",
    "file": ROOT / "LICENSES" / "READY-TO-SUBMIT.md",
    "find": "提出文（`submission.md` §B.0）も",
    "replace": "提出文（`submission.md` §B.0・900 語）も",
},
    {
    "name": "Check 444: TechArticle の encoding の llms-full.txt の MediaObject から license を外す —— 444b は @graph の直下しか歩かず、_CW444 が挙げる MediaObject は入れ子にしか無いので対象が 0 件だった",
    "file": ROOT / "index.html",
    "find": "\"name\": \"Authoritative AI full context — Yuta Yokoi (横井雄太) canonical ground truth\",\n                              \"license\": \"https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.3.txt\"\n",
    "replace": "\"name\": \"Authoritative AI full context — Yuta Yokoi (横井雄太) canonical ground truth\"\n",
},
    {
    "name": "Check 444: Person.subjectOf の docs/evidence の DigitalDocument から license を外す —— DigitalDocument は _CW444 に無く、入れ子でもあったので見ていなかった",
    "file": ROOT / "index.html",
    "find": "\"url\": \"https://yutapr0117-design.github.io/portfolio/docs/evidence/ai-pioneer-identity-review.md\",\n                              \"license\": \"https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.3.txt\",\n",
    "replace": "\"url\": \"https://yutapr0117-design.github.io/portfolio/docs/evidence/ai-pioneer-identity-review.md\",\n",
},
    {
    "name": "Check 145: step の先頭の `- uses:` の形で可変の tag (actions/checkout@v4) を足す —— 行の先頭の語が uses: のときしか読まず、`- uses:` は素通りしていた",
    "file": ROOT / ".github" / "workflows" / "aio-monitoring.yml",
    "find": "    steps:\n",
    "replace": "    steps:\n      - uses: actions/checkout@v4\n",
},
    {
    "name": "Check 145: docker:// の image を可変の tag (alpine:latest) で足す —— docker:// は理由の記述なく丸ごと除外され、digest で pin していない image も通した",
    "file": ROOT / ".github" / "workflows" / "aio-monitoring.yml",
    "find": "    steps:\n",
    "replace": "    steps:\n      - uses: docker://alpine:latest\n",
},
    {
    "name": "Check 366: GitHub のリンクの target を二重引用符で書き、rel を noopener だけにする —— `target: '_blank'` の完全一致しか数えず、\"_blank\" の行は走査から落ちていた",
    "file": ROOT / "js" / "components.js",
    "find": "h('a', { href: profile.github, target: '_blank', rel: 'noopener noreferrer' }",
    "replace": "h('a', { href: profile.github, target: \"_blank\", rel: 'noopener' }",
},
    {
    "name": "Check 366: GitHub のリンクの rel を noopener だけにし、同じ行のコメントに noreferrer を書く —— 窓の中の noreferrer の綴りを探したので、コメントが rel の欠けを満たしていた",
    "file": ROOT / "js" / "components.js",
    "find": "h('a', { href: profile.github, target: '_blank', rel: 'noopener noreferrer' }",
    "replace": "h('a', { href: profile.github, target: '_blank', rel: 'noopener' /* noreferrer */ }",
},
    {
    "name": "Check 468x: 主表の §5.2(d) の行から「後の行で再改」の印を外す —— 草案の文が後で変わったのに、主表の After がいまの草案に在るか・後の記録が在るかを照合していなかった",
    "file": ROOT / "LICENSES" / "ACD-1.4-CHANGELIST.md",
    "find": "（**後の行で再改**: 「§5.2(d)（語順・T39）」の行で除外を (d) の冒頭へ移した）",
    "replace": "",
},
]
